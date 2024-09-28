from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.segments.validation.segment_validator import SegmentValidator
from youtube_autonomous.shortcodes.objects.shortcode_tag import ShortcodeTag, ShortcodeType
from youtube_autonomous.project import Project
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER, DEFAULT_PROJECTS_OUTPUT_FOLDER
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from yta_general_utils.temp import clean_temp_folder
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.path import create_file_abspath
from yta_general_utils.file.reader import read_json_from_file
from yta_general_utils.logger import print_completed, print_in_progress
from typing import Union


class YoutubeAutonomous:
    __database_handler: DatabaseHandler = None
    """
    Object to interact with the database and get and create projects.

    _This parameter is not manually set by the user._
    """
    __segment_validator: SegmentValidator = None
    """
    Object to validate the segments we want to use to build a project.

    _This parameter is not manually set by the user._
    """
    __segments_abspath: Union[str, None] = None
    """
    The absolute path that points to the segments folder in which this
    software will store the segments related content parts that are
    created during the whole segment building process. This folder 
    allows us recovering a non-finished project in which we generated
    some segments in the past but not all of them.

    _This parameter is not manually set by the user._
    """
    __projects_output_abspath: Union[str, None] = None
    """
    The absolute path that points to the projects output folder in which
    this software will store the final videos generated.

    _This parameter is not manually set by the user._
    """

    def __init__(self):
        """
        Initializes the object and creates the segment part building
        folder in which segment parts will be stored.
        """
        self.__database_handler = DatabaseHandler()
        self.__segment_validator = SegmentValidator()

        self.__segments_abspath = get_project_abspath() + DEFAULT_SEGMENT_PARTS_FOLDER + '/'
        self.__projects_output_abspath = get_project_abspath() + DEFAULT_PROJECTS_OUTPUT_FOLDER + '/'

        # We force to create the folder if it doesn't exist
        create_file_abspath(self.__segments_abspath + 'toforce')
        create_file_abspath(self.__projects_output_abspath + 'toforce')

    def purge(self, do_remove_segments_files = False):
        """
        Cleans the temporary folder removing all previous generated 
        temporary files, and also the segment files if the
        'do_remove_segments_files' parameter is set to True.
        """
        clean_temp_folder()
        if do_remove_segments_files:
            # TODO: Remove all files in self.__segments_abspath folder
            pass

    def check_config(self):
        # TODO: Check that he config is ok
        pass
     
    def insert_project_in_database_from_file(self, filename: str):
        """
        Reads the provided project content 'filename' and creates a new 
        project in the database if the provided 'filename' contains a new
        project and is valid. If the information belongs to an already
        registered project, it will raise an exception.

        This method returns the new stored project mongo ObjectId if 
        successfully stored, or raises an Exception if anything went wrong.
        """
        if not filename:
            raise Exception('We need a project content "filename" to create a new project.')
        
        if not isinstance(filename, str):
            raise Exception('The "filename" parameter provided is a str.')
        
        json_data = self.__read_project_from_file(filename)

        # If a project with the same content exists, it is the same project
        db_project = self.__database_handler.get_database_project_from_json(json_data)
        if db_project:
            raise Exception('There is an existing project in the database with the same content.')

        # TODO: Process the information to store it parsed
        json_data = self.check_and_prepare_data(json_data)

        db_project = self.__database_handler.insert_project(json_data)

        print_completed('Project created in database with ObjectId = "' + str(db_project['_id']) + '"')

        return str(db_project['_id'])
    
    def validate_data(self, json_data: dict):
        segments = json_data.get('segments', [])

        if not segments:
            raise Exception('No "segments" in the provided "json_data" parameter.')

        # TODO: Check main structure and validate fields
        # TODO: This shortcode parser must have the definitive shortcodes
        # TODO: Shortcode handlers must be working, check Notion (https://www.notion.so/ShortcodeParser-personalizado-10ff5a32d462804d9253e9cb782e5540?pvs=4)
        shortcode_parser = ShortcodeParser([ShortcodeTag('meme', ShortcodeType.SIMPLE)])

        from youtube_autonomous.elements.rules.element_rules import ElementRules
        from youtube_autonomous.segments.enums import SegmentType

        for segment in segments:
            type = json_data.get('type', '')

            if not type or not SegmentType.is_valid(type):
                raise Exception('The "type" provided is not valid.')

            # 1. If 'text' have shortcodes
            # We use an empty shortcode parser to accept no shortcodes
            # so any shortcode found will raise an Exception
            ShortcodeParser([]).parse(segment.get('text', ''))

            # 2. If 'narration_text' have invalid shortcodes
            # The final shortcode will parse only the accepted shortcodes
            # so if any unknown shortcode appears it will raise an Exception
            shortcode_parser.parse(segment.get('narration_text', ''))

            # 3. If 'data.effects' are invalid
            from youtube_autonomous.elements.rules.effect_element_rules import EffectElementRules
            from youtube_autonomous.elements.rules.greenscreen_element_rules import GreenscreenElementRules
            from youtube_autonomous.elements.rules.rules_checker import RulesChecker
            # TODO: This must be const or something like that
            accepted_fields = ['greenscreens', 'effects']
            # TODO: Delete any other field that is not one of above list
            for enhancement in segment.get('enhancements', []):
                effects = enhancement.get('effects', [])
                for effect in effects:
                    RulesChecker(EffectElementRules()).check_this_need_rules(effect)

                greenscreens = enhancement.get('greenscreens', [])
                for greenscreen in greenscreens:
                    RulesChecker(GreenscreenElementRules()).check_this_need_rules(greenscreen)

                # TODO: We should check any other thing that is here (frames, etc.)

            # 4. If doesn't have necessary fields for its type
            rules_checker = RulesChecker(ElementRules.get_rules_class_by_type(type))
            rules_checker.check_this_need_rules(segment)

    
    def check_and_prepare_data(self, json_data: dict):
        self.validate_data(json_data)

        shortcode_parser = ShortcodeParser()
        for segment in json_data['segments']:
            # 1. Parse shortcodes of 'narration_text' if existing
            if segment['narration_text']:
                shortcode_parser.parse(segment['narration_text'])
                segment['narration_text_sanitized_without_shortcodes'] = shortcode_parser.narration_text_sanitized_without_shortcodes
                segment['narration_text_with_simplified_shortcodes'] = shortcode_parser.narration_text_with_simplified_shortcodes
                segment['narration_text_sanitized'] = shortcode_parser.narration_text_sanitized

            if segment['duration'] and isinstance(segment['duration'], str):
                # TODO: Make this consts and/or Enum
                if segment['duration'] == 'SHORTCODE_CONTENT':
                    segment['duration'] = 99997
                elif segment['duration'] == 'FILE_DURATION':
                    segment['duration'] = 99998
                elif segment['duration'] == 'SEGMENT_DURATION':
                    segment['duration'] = 99999
    
    def process_unfinished_projects(self):
        db_projects = self.get_unfinished_projects()

        for db_project in db_projects:
            print_in_progress(f'Processing project "{db_project["_id"]}"')
            self.process_project(db_project)
            print_completed(f'Project "{db_project["_id"]}" processed succesfully!')

    def process_project(self, db_project):
        project = Project(db_project['_id'], db_project['status'], db_project['segments'])
        project.build(f'{self.__projects_output_abspath}project_{project.id}.mp4')
    
    # TODO: This below is for testing, remove it
    def get_unfinished_project(self):
        """
        Returns the first unfinished project that exists in the
        database, or None if there are no unfinished projects.
        """
        return self.__database_handler.get_unfinished_project()

    def get_unfinished_projects(self):
        """
        Returns a list containing all the existing projects in the 
        database that have not been finished yet, or an empty list
        if there are no unfinished projects.
        """
        return self.__database_handler.get_unfinished_projects()
    
    def __read_project_from_file(self, filename: str):
        """
        Reads the provided 'filename', that should contain the information of
        a project, and validates its content and structure. This method will
        return the data read as a dict or will raise an Exception if something
        is not ok.
        """
        if not filename:
            raise Exception('No "filename" provided.')
        
        if not isinstance(filename, str):
            raise Exception('The "filename" parameter provided is a str.')
        
        json_data = read_json_from_file(filename)

        if not 'segments' in json_data:
            raise Exception('The provided "filename" does not contain the expected data structure.')

        # We validate each segment to be able to store the project
        # This will raise an Exception if something is not ok
        for segment in json_data['segments']:
            self.__segment_validator.validate(segment)

        return json_data

    # TODO: Apply ObjectId type to 'project_id'
    def __get_project_from_database_by_id(self, project_id):
        """
        Gets the project with the provided 'project_id' if existing, or
        None if not.
        """
        return self.__database_handler.get_database_project_from_id(project_id)
    
    # TODO: Apply json type to 'json'
    def __get_project_from_database_by_json(self, json):
        """
        Gets the project with the provided 'json' if existing, or None if
        not. This 'json' will be compared with the 'script' field stored
        in database to check if there is a similar project previously 
        stored that must be recovered instead of duplicating it.
        """
        return self.__database_handler.get_database_project_from_json(json)
