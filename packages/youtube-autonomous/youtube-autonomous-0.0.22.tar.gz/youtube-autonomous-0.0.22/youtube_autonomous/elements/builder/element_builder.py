from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.enums import SegmentType
from youtube_autonomous.elements.validator import BUILDER_SUBCLASSES
from youtube_autonomous.segments.builder.ai import create_ai_narration
from typing import Union


class ElementBuilder:
    @staticmethod
    def get_subclasses():
        from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
        from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
        from youtube_autonomous.elements.builder.ai_video_element_builder import AIVideoElementBuilder
        from youtube_autonomous.elements.builder.video_element_builder import VideoElementBuilder
        from youtube_autonomous.elements.builder.custom_stock_element_builder import CustomStockElementBuilder
        from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
        from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
        from youtube_autonomous.elements.builder.sound_element_builder import SoundElementBuilder
        from youtube_autonomous.elements.builder.youtube_video_element_builder import YoutubeVideoElementBuilder
        from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
        from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder
        from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
        from youtube_autonomous.elements.builder.greenscreen_element_builder import GreenscreenElementBuilder

        return [
            AIImageElementBuilder,
            AIVideoElementBuilder,
            ImageElementBuilder,
            VideoElementBuilder,
            CustomStockElementBuilder,
            StockElementBuilder,
            MemeElementBuilder,
            SoundElementBuilder,
            YoutubeVideoElementBuilder,
            TextElementBuilder,
            PremadeElementBuilder,
            EffectElementBuilder,
            GreenscreenElementBuilder
        ]

    @staticmethod
    def get_subclasses_as_str():
        return ', '.join(ElementBuilder.get_subclasses())
    
    @staticmethod
    def get_subclass_by_type(type: Union[SegmentType, str]):
        type = ElementParameterValidator.validate_segment_type(type)

        from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
        from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
        from youtube_autonomous.elements.builder.ai_video_element_builder import AIVideoElementBuilder
        from youtube_autonomous.elements.builder.video_element_builder import VideoElementBuilder
        from youtube_autonomous.elements.builder.custom_stock_element_builder import CustomStockElementBuilder
        from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
        from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
        from youtube_autonomous.elements.builder.sound_element_builder import SoundElementBuilder
        from youtube_autonomous.elements.builder.youtube_video_element_builder import YoutubeVideoElementBuilder
        from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
        from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder
        from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
        from youtube_autonomous.elements.builder.greenscreen_element_builder import GreenscreenElementBuilder

        if type == SegmentType.MEME:
            return MemeElementBuilder
        elif type == SegmentType.AI_IMAGE:
            return AIImageElementBuilder
        elif type == SegmentType.AI_VIDEO:
            return AIVideoElementBuilder
        elif type == SegmentType.IMAGE:
            return ImageElementBuilder
        elif type == SegmentType.VIDEO:
            return VideoElementBuilder
        elif type == SegmentType.STOCK:
            return StockElementBuilder
        elif type == SegmentType.CUSTOM_STOCK:
            return CustomStockElementBuilder
        elif type == SegmentType.SOUND:
            return SoundElementBuilder
        elif type == SegmentType.YOUTUBE_VIDEO:
            return YoutubeVideoElementBuilder
        elif type == SegmentType.TEXT:
            return TextElementBuilder
        elif type == SegmentType.PREMADE:
            return PremadeElementBuilder
        elif type == SegmentType.EFFECT:
            return EffectElementBuilder
        elif type == SegmentType.GREENSCREEN:
            return GreenscreenElementBuilder
    
    @classmethod
    def build_narration(cls, text: str, output_filename: str):
        """
        Generates a narration file that narrates the 'text' provided and
        is stored locally as 'output_filename'. If 'text' or 
        'output_filename' fields are not provided it will raise an 
        Exception.
        """
        ElementParameterValidator.validate_string_mandatory_parameter(text)
        ElementParameterValidator.validate_string_mandatory_parameter(output_filename)

        return create_ai_narration(text, output_filename = output_filename)
    
    @classmethod
    def handle_narration_from_segment(cls, segment: dict):
        pass