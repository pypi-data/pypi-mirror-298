from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import SegmentField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from yta_general_utils.file.filename import FileType
from yta_general_utils.downloader.video import download_video
from moviepy.editor import VideoFileClip
from typing import Union


class VideoElementBuilder(ElementBuilder):
    @classmethod
    def build_from_segment(cls, segment: dict):
        filename = segment.get(SegmentField.FILENAME.value, None)
        url = segment.get(SegmentField.URL.value, None)
         # TODO: I should always have 'calculated_duration' when duration
        # has been processed
        duration = segment.get('calculated_duration', None)

        # TODO: What about this strategy. Do we apply the strategy here or
        # should get the call when its been applied (?)
        # By now I'm applying it here, feel free to change this in when
        # you know
        if filename and url:
            return cls.build_from_filename(filename)
        elif url:
            return cls.build_from_url(url)
        
        raise Exception('No "url" nor "filename" provided.')

    @classmethod
    def build_from_filename(cls, filename: str, duration: Union[float, int]):
        ElementParameterValidator.validate_filename(filename, FileType.VIDEO)
        ElementParameterValidator.validate_duration(duration)

        return VideoFileClip(filename)

    @classmethod
    def build_from_url(cls, url: str, duration: Union[float, int]):
        ElementParameterValidator.validate_url(url)
        ElementParameterValidator.validate_duration(duration)

        # TODO: Try to do all this process in memory, writting not the video
        filename = download_video(url)

        return VideoFileClip(filename)