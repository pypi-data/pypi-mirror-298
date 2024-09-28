from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.builder.ai import create_ai_narration


class ElementBuilder:
    @classmethod
    def get_subclasses(cls):
        """
        Returns all the existing subclasses of ElementBuilder.
        """
        from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
        from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
        from youtube_autonomous.elements.builder.ai_video_element_builder import AIVideoElementBuilder
        from youtube_autonomous.elements.builder.video_element_builder import VideoElementBuilder
        from youtube_autonomous.elements.builder.custom_stock_element_builder import CustomStockElementBuilder
        from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
        from youtube_autonomous.elements.builder.sound_element_builder import SoundElementBuilder
        from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
        from youtube_autonomous.elements.builder.youtube_video_element_builder import YoutubeVideoElementBuilder
        from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
        from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder

        return [
            ImageElementBuilder,
            AIImageElementBuilder,
            VideoElementBuilder,
            AIVideoElementBuilder,
            CustomStockElementBuilder,
            StockElementBuilder,
            SoundElementBuilder,
            MemeElementBuilder,
            YoutubeVideoElementBuilder,
            TextElementBuilder,
            PremadeElementBuilder
        ]
    
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