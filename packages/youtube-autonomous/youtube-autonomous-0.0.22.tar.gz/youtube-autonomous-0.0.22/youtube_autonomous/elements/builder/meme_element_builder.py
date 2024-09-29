from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import SegmentField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.youtube.youtube_downloader import YoutubeDownloader
from moviepy.editor import VideoFileClip
from typing import Union


class MemeElementBuilder(ElementBuilder):
    @classmethod
    def build_from_segment(cls, segment: dict):
        keywords = segment.get(SegmentField.KEYWORDS.value, None)
        # TODO: I should always have 'calculated_duration' when duration
        # has been processed
        duration = segment.get('calculated_duration', None)

        return cls.build(keywords, duration)

    @classmethod
    def build(cls, keywords: str, duration: Union[float, int]):
        ElementParameterValidator.validate_keywords(keywords)
        ElementParameterValidator.validate_duration(duration)

        youtube_downloader = YoutubeDownloader()

        youtube_downloader.deactivate_ignore_repeated()
        temp_filename = youtube_downloader.download_meme_video(keywords, True, True)
        youtube_downloader.activate_ignore_repeated()

        # TODO: Look for a better strategy (?)
        if not temp_filename:
            raise Exception('No meme found with the given "keywords": ' + str(keywords) + '.')
        
        video = VideoFileClip(temp_filename)

        # TODO: I apply the duration but I don't change it
        if duration < video.duration:
            video = video.subclip(0, duration)