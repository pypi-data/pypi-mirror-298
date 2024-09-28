from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import SegmentField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator


class AIVideoElementBuilder(ElementBuilder):
    """
    Builder to obtain videos generated with AI.
    """
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

        raise Exception('Functionality not implemented yet.')

        # TODO: Build a video from some AI
        # video = create_ai_video(keywords, duration)

        return video