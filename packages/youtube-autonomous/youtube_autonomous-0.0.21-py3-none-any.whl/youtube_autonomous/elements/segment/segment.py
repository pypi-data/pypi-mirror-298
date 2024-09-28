from youtube_autonomous.segments.enums import SegmentType, SegmentField, EnhancementElementDuration
from youtube_autonomous.elements.meme_element import MemeElement
from youtube_autonomous.elements.element_data import ElementData
from youtube_autonomous.database.database_handler import DatabaseHandler
from youtube_autonomous.shortcodes.shortcode_parser import ShortcodeParser
from youtube_autonomous.segments.builder.ai import create_ai_narration
from youtube_autonomous.shortcodes.objects.shortcode import Shortcode
from yta_general_utils.logger import print_in_progress, print_completed
from yta_general_utils.file import copy_file
from yta_general_utils.file.filename import get_file_extension
from moviepy.editor import VideoFileClip, AudioFileClip
from bson.objectid import ObjectId
from typing import Union


class Segment:
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status: str):
        self._status = status
        if self._do_update_database:
            self.database_handler.update_project_segment_status(self.project_id, self.index, status)

    @property
    def audio_filename(self):
        audio_filename = self.data.audio_filename

        if audio_filename and not self.audio_clip:
            self.audio_clip = AudioFileClip(audio_filename)

        return audio_filename
    
    @audio_filename.setter
    def audio_filename(self, audio_filename: Union[str, None]):
        self.data.audio_filename = audio_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, SegmentField.AUDIO_FILENAME.value, audio_filename)

        if self.data.audio_filename:
            self.audio_clip = AudioFileClip(self.data.audio_filename)

    @property
    def video_filename(self):
        video_filename = self.data.video_filename

        if video_filename and not self.video_clip:
            self.video_clip = VideoFileClip(video_filename)

        return video_filename
    
    @video_filename.setter
    def video_filename(self, video_filename: Union[str, None]):
        self.data.video_filename = video_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, SegmentField.VIDEO_FILENAME.value, video_filename)

        if self.data.video_filename:
            self.video_clip = VideoFileClip(self.data.video_filename)

    @property
    def full_filename(self):
        full_filename = self.data.full_filename

        if full_filename and not self.full_clip:
            self.full_clip = VideoFileClip(full_filename)

        return full_filename
    
    @full_filename.setter
    def full_filename(self, full_filename: Union[str, None]):
        self.data.full_filename = full_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, SegmentField.FULL_FILENAME.value, full_filename)

        if self.data.full_filename:
            self.full_clip = VideoFileClip(self.data.full_filename)

    @property
    def audio_narration_filename(self):
        return self.data.audio_narration_filename
    
    @audio_narration_filename.setter
    def audio_narration_filename(self, audio_narration_filename: Union[str, None]):
        self.data.audio_narration_filename = audio_narration_filename

        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, SegmentField.AUDIO_NARRATION_FILENAME.value, audio_narration_filename)

    @property
    def transcription(self):
        return self.data.transcription
    
    @transcription.setter
    def transcription(self, transcription: Union[dict, None]):
        self.data.transcription = transcription
        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'transcription', transcription)

    @property
    def shortcodes(self):
        return self.data.shortcodes
    
    @shortcodes.setter
    def shortcodes(self, shortcodes: Union[list[Shortcode], None]):
        self.data.shortcodes = shortcodes
        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'shortcodes', shortcodes)

    @property
    def calculated_duration(self):
        return self.data.calculated_duration
    
    @calculated_duration.setter
    def calculated_duration(self, calculated_duration: Union[float, int, None]):
        self.data.calculated_duration = calculated_duration
        if self._do_update_database:
            self.database_handler.update_project_segment_field(self.project_id, self.index, 'calculated_duration', calculated_duration)

    @property
    def text(self):
        return self.data.text
    
    @property
    def narration_text(self):
        return self.data.narration_text

    def __init__(self, project_id: Union[str, ObjectId], index: int, type: Union[str, SegmentType], status: str, data: dict):
        if not type:
            raise Exception('No "type" provided.')
        
        if isinstance(type, str):
            if not SegmentType.is_valid(type):
                raise Exception('The "type" provided is not a valid SegmentType.')
            
            type = SegmentType(type)

        # TODO: Check 'data'

        self._do_update_database = False

        self.type = type
        self.project_id = str(project_id)
        self.index = index
        self.status = status
        
        if self.type == SegmentType.MEME:
            self.element = MemeElement()
            self.data = ElementData(data)

        self.database_handler = DatabaseHandler()
        self.shortcode_parser = ShortcodeParser()

        self.effects = data.get('effects', [])

        self._do_update_database = True

    def validate(self):
        # 1. If 'text' have shortcodes
        self.shortcode_parser.parse(self.text)

        # 2. If 'narration_text' have invalid shortcodes
        self.shortcode_parser.parse(self.narration_text)

        # 3. If 'data.effects' are invalid
        from youtube_autonomous.elements.rules.effect_element_rules import EffectElementRules
        from youtube_autonomous.elements.rules.rules_checker import RulesChecker
        for effect in self.effects:
            RulesChecker(EffectElementRules()).check_this_need_rules(effect)
        # TODO: I need to check any other modification I let them
        # use, such as Greenscreens, etc.

        # 4. If element has not necessary parameters
        self.element.rules_checker.check_this_need_rules(self.data)

    def prepare(self):
        # Check duration
        # TODO: This has to be done when storing the project
        if self.data.duration and not self.calculated_duration:
            if isinstance(self.data.duration, str):
                # TODO: Make this consts and/or Enum
                if self.data.duration == 'SHORTCODE_CONTENT':
                    self.data.duration = 99997
                elif self.data.duration == 'FILE_DURATION':
                    self.data.duration = 99998
                elif self.data.duration == 'SEGMENT_DURATION':
                    self.data.duration = 99999
            self.calculated_duration = self.data.duration

        # Parse narration text and remove shortcodes
        # TODO: This has to be done when storing the project
        if self.element.rules_checker.should_build_narration_rule(self.data) and not self.data.narration_text_sanitized_without_shortcodes:
            self.shortcode_parser.parse(self.data.narration_text)
            self.data.narration_text_sanitized_without_shortcodes = self.shortcode_parser.text_sanitized_without_shortcodes
            # TODO: I think these 2 below are useless
            self.data.narration_text_with_simplified_shortcodes = self.shortcode_parser.text_sanitized_with_simplified_shortcodes
            self.data.narration_text_sanitized = self.shortcode_parser.text_sanitized

        # Generate narration audio
        if self.element.rules_checker.should_build_narration_rule(self.data) and not self.audio_clip:
            self.handle_narration()

        # Generate video
        if not self.video_clip:
            self.video_clip = self._builder.build_segment(self)
            # We write this video part to be able to recover it in the future
            segment_part_filename = self.__create_segment_file('video.mp4')
            self.video_clip.write_videofile(segment_part_filename)
            self.video_filename = segment_part_filename
            print_completed('Created basic video part and stored locally and in database.')


        



    def handle_narration(self):
        if self.audio_narration_filename:
            segment_part_filename = self.__create_segment_file(f'narration.{get_file_extension(self.audio_narration_filename)}')
            copy_file(self.audio_narration_filename, segment_part_filename)
            print_completed('Original voice narration file copied to segment parts folder')
            self.audio_narration_filename = segment_part_filename
            self.audio_filename = segment_part_filename
        else:
            segment_part_filename = self.__create_segment_file('narration.wav')
            # TODO: Voice parameter need to change
            self.audio_filename = create_ai_narration(self.data.narration_text_sanitized_without_shortcodes, output_filename = segment_part_filename)
            print_completed('Voice narration created successfully')

    def build(self):
        pass


    def __create_segment_file(self, filename: str):
        """
        Creates a filename within the definitive segments folder
        to keep the generated file locally to recover it in the
        next project execution if something goes wrong. The 
        definitive filename will be built using the provided
        'filename' and adding some more information in the name.

        This method will generate a temporary filename that uses
        the current segment index in its name and is placed in 
        segment parts folder.

        This method returns the final filename created.
        """
        if not filename:
            raise Exception('No "filename" provided.')

        temp_filename = get_temp_filename(filename)

        return f'{DEFAULT_SEGMENT_PARTS_FOLDER}/segment_{self.segment_index}_{temp_filename}'