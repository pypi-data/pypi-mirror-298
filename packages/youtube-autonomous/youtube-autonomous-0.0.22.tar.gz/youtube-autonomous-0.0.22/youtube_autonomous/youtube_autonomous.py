from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.segments.validation.segment_validator import SegmentValidator
from youtube_autonomous.shortcodes.objects.shortcode_tag import ShortcodeTag, ShortcodeType
from youtube_autonomous.project import Project
from youtube_autonomous.segments.enums import SegmentField, EnhancementField, ProjectStatus, SegmentStatus
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.config import DEFAULT_SEGMENT_PARTS_FOLDER, DEFAULT_PROJECTS_OUTPUT_FOLDER
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from yta_general_utils.temp import clean_temp_folder
from yta_general_utils.programming.path import get_project_abspath
from yta_general_utils.path import create_file_abspath
from yta_general_utils.file.reader import read_json_from_file
from yta_general_utils.logger import print_completed, print_in_progress, print_error
from datetime import datetime
from typing import Union

import copy


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

        for index, segment in enumerate(segments):
            print_in_progress(f'Handling segment [{index}]')
            type = ElementParameterValidator.validate_segment_type(segment.get('type', '')).value
            # TODO: Type can be unavailable for 'Segment', check that

            # 1. If 'text' have shortcodes
            # We use an empty shortcode parser to accept no shortcodes
            # so any shortcode found will raise an Exception
            try:
                ShortcodeParser([]).parse(segment.get('text', ''))
            except Exception as e:
                #print(e)
                print_error('Field "text" not found or shortcodes found on it.')
                exit()

            # 2. If 'narration_text' have invalid shortcodes
            # The final shortcode will parse only the accepted shortcodes
            # so if any unknown shortcode appears it will raise an Exception
            try:
                shortcode_parser.parse(segment.get('narration_text', ''))
            except Exception as e:
                #print(e)
                print_error('Field "narration_text" not found or unregistered shortcodes found on it.')
                exit()

            # X. Parse string duration to check if valid
            # TODO: Implement constants from somewhere
            if segment.get('duration', None) and isinstance(segment['duration'], str) and segment['duration'] not in ['SHORTCODE_CONTENT', 'FILE_DURATION', 'SEGMENT_DURATION']:
                    raise Exception(f'Unexpected duration value {segment["duration"]}.')

            # 3. If 'data.effects' are invalid
            from youtube_autonomous.elements.rules.effect_element_rules import EffectElementRules
            from youtube_autonomous.elements.rules.greenscreen_element_rules import GreenscreenElementRules
            from youtube_autonomous.elements.rules.rules_checker import RulesChecker
            # TODO: This must be const or something like that

            # We let the user know if any unaccepted field has been given
            # and we raise and Exception if that happen
            accepted_fields = SegmentField.get_all_values() + ['enhancements']
            accepted_fields_str = ', '.join(accepted_fields)
            unaccepted_fields = [key for key in segment.keys() if key not in accepted_fields]
            unaccepted_fields_str = ', '.join(unaccepted_fields)
            if unaccepted_fields:
                raise Exception(f'The next fields are not accepted by our system: "{unaccepted_fields_str}". The ones accepted are these: "{accepted_fields_str}"')
            
            for index, enhancement in enumerate(segment.get('enhancements', [])):
                print_in_progress(f'   Handling enhancement [{index}]')
                enhancement_type = ElementParameterValidator.validate_segment_type(enhancement.get('type', '')).value
                # TODO: Type can be unavailable for 'EnhancementElement', check that
                # 1. If 'text' have shortcodes
                # We use an empty shortcode parser to accept no shortcodes
                # so any shortcode found will raise an Exception
                try:
                    ShortcodeParser([]).parse(enhancement.get('text', ''))
                except Exception as e:
                    #print(e)
                    print_error('Field "text" not found or shortcodes found on it.')
                    exit()

                # 2. If 'narration_text' have invalid shortcodes
                # The final shortcode will parse only the accepted shortcodes
                # so if any unknown shortcode appears it will raise an Exception
                try:
                    shortcode_parser.parse(enhancement.get('narration_text', ''))
                except Exception as e:
                    #print(e)
                    print_error('Field "narration_text" not found or unregistered shortcodes found on it.')
                    exit()

                # X. Parse string duration to check if valid
                # TODO: Implement constants from somewhere
                accepted_str_duration = ['SHORTCODE_CONTENT', 'FILE_DURATION', 'SEGMENT_DURATION']
                accepted_str_duration_str = ', '.join(accepted_str_duration)
                if enhancement.get('duration', None) and isinstance(enhancement['duration'], str) and enhancement['duration'] not in accepted_str_duration:
                        raise Exception(f'Unexpected duration value {enhancement["duration"]}. The accepted strings are: {accepted_str_duration_str}')

                 # We let the user know if any unaccepted field has been given
                # and we raise and Exception if that happen
                accepted_fields = EnhancementField.get_all_values()
                accepted_fields_str = EnhancementField.get_all_values_as_str()
                unaccepted_fields = [key for key in enhancement.keys() if key not in accepted_fields]
                unaccepted_fields_str = ', '.join(unaccepted_fields)
                if unaccepted_fields:
                    raise Exception(f'The next fields are not accepted by our system: "{unaccepted_fields_str}". The ones accepted are these: "{accepted_fields_str}"')

                rules_checker = RulesChecker(ElementRules.get_subclass_by_type(enhancement_type)())
                rules_checker.check_this_need_rules(enhancement)

                # TODO: We should check any other thing that is here (frames, etc.)

            # 4. If doesn't have necessary fields for its type
            rules_checker = RulesChecker(ElementRules.get_subclass_by_type(type)())
            rules_checker.check_this_need_rules(segment)

    
    def prepare_data_to_database(self, json_data: dict):
        """
        This method prepares the project data that has been previously
        verified so it has the structure with it will be stored in the
        database.

        This method will parse the 'narration_text' and generate the
        some processed and sanitized fields (it processes the 
        shortcodes). It will also transform any string type duration
        to its actual numeric value that will be dynamically processed
        later when building the content.

        The result of this method will be a dict containing 'status',
        'script' and 'segments' fields.
        """
        data = {
            'status': ProjectStatus.TO_START.value,
            'script': copy.deepcopy(json_data),
            'segments': None
        }

        shortcode_parser = ShortcodeParser([])
        segments = []
        for segment in json_data['segments']:
            # Manually handle 'narration_text'
            if segment.get('narration_text', ''):
                shortcode_parser.parse(segment['narration_text'])
                segment['narration_text_sanitized_without_shortcodes'] = shortcode_parser.text_sanitized_without_shortcodes
                segment['narration_text_with_simplified_shortcodes'] = shortcode_parser.text_sanitized_with_simplified_shortcodes
                segment['narration_text_sanitized'] = shortcode_parser.text_sanitized

            # Manually handle string duration
            if segment.get('duration', None) and isinstance(segment['duration'], str):
                # TODO: Make this consts and/or Enum
                if segment['duration'] == 'SHORTCODE_CONTENT':
                    segment['duration'] = 99997
                elif segment['duration'] == 'FILE_DURATION':
                    segment['duration'] = 99998
                elif segment['duration'] == 'SEGMENT_DURATION':
                    segment['duration'] = 99999
                    
            segment['status'] = SegmentStatus.TO_START.value
            segment['created_at'] = datetime.now()

            for enhancement in segment.get('enhancements', []):
                # Manually handle 'narration_text'
                if enhancement.get('narration_text', ''):
                    shortcode_parser.parse(enhancement['narration_text'])
                    enhancement['narration_text_sanitized_without_shortcodes'] = shortcode_parser.text_sanitized_without_shortcodes
                    enhancement['narration_text_with_simplified_shortcodes'] = shortcode_parser.text_sanitized_with_simplified_shortcodes
                    enhancement['narration_text_sanitized'] = shortcode_parser.text_sanitized

                # Manually handle string duration
                if enhancement.get('duration', None) and isinstance(enhancement['duration'], str):
                    # TODO: Make this consts and/or Enum
                    if enhancement['duration'] == 'SHORTCODE_CONTENT':
                        enhancement['duration'] = 99997
                    elif enhancement['duration'] == 'FILE_DURATION':
                        enhancement['duration'] = 99998
                    elif enhancement['duration'] == 'SEGMENT_DURATION':
                        enhancement['duration'] = 99999

                enhancement['status'] = SegmentStatus.TO_START.value
                enhancement['created_at'] = datetime.now()

            segments.append(segment)

        # This is the structure the project must have in database
        data['segments'] = segments

        return data

    def check_and_prepare_data(self, json_data: dict):
        """
        This method will validate the 'json_data' provided and raise
        an Exception if anything is wrong. If it is ok, it will 
        process the data and turn it into the expected data to be 
        stored in the database.
        """
        self.validate_data(json_data)
        return self.prepare_data_to_database(json_data)
        
    
    def process_unfinished_projects(self):
        db_projects = self.get_unfinished_projects()

        for db_project in db_projects:
            print_in_progress(f'Processing project "{db_project["_id"]}"')
            self.process_project(db_project)
            print_completed(f'Project "{db_project["_id"]}" processed succesfully!')

    def process_project(self, db_project):
        project = Project(db_project['_id'])
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
        # for segment in json_data['segments']:
        #     self.__segment_validator.validate(segment)

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
