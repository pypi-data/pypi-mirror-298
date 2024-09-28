from yta_general_utils.programming.parameter_validator import ParameterValidator
from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.elements.rules.ai_image_element_rules import AIImageElementRules
from youtube_autonomous.elements.rules.image_element_rules import ImageElementRules
from youtube_autonomous.elements.rules.meme_element_rules import MemeElementRules
from youtube_autonomous.elements.rules.ai_video_element_rules import AIVideoElementRules
from youtube_autonomous.elements.rules.video_element_rules import VideoElementRules
from youtube_autonomous.elements.rules.sound_element_rules import SoundElementRules
from youtube_autonomous.elements.rules.custom_stock_element_rules import CustomStockElementRules
from youtube_autonomous.elements.rules.stock_element_rules import StockElementRules
from youtube_autonomous.elements.rules.youtube_video_element_rules import YoutubeVideoElementRules
from youtube_autonomous.elements.rules.text_element_rules import TextElementRules
from youtube_autonomous.elements.rules.premade_element_rules import PremadeElementRules
from youtube_autonomous.elements.builder.element_builder import ElementBuilder
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
from youtube_autonomous.elements.validator.error_message import ErrorMessage
from yta_general_utils.file.filename import FileType
from typing import Union


class ElementParameterValidator(ParameterValidator):
    @classmethod
    def validate_keywords(cls, keywords: str):
        return cls.validate_string_mandatory_parameter('keywords', keywords)

    @classmethod
    def validate_text(cls, text: str):
        return cls.validate_string_mandatory_parameter('text', text)
    
    @classmethod
    def validate_premade_name(cls, premade_name: str):
        # TODO: Maybe validate that is a key of a valid premade (?)
        return cls.validate_string_mandatory_parameter('premade_name', premade_name)
    
    @classmethod
    def validate_text_class_name(cls, text_class_name: str):
        return cls.validate_string_mandatory_parameter('text_class_name', text_class_name)
    
    @classmethod
    def validate_duration(cls, duration: Union[int, float]):
        # TODO: Maybe validate that is a key of a valid text class (?)
        return cls.validate_numeric_positive_mandatory_parameter('duration', duration)
    
    @classmethod
    def validate_url(cls, url: str, is_mandatory: True):
        """
        A mandatory 'url' must be not None, a valid string and also
        a valid url and accessible.

        A non mandatory 'url' can be None, 
        """
        if not is_mandatory and not url:
            return True
        
        cls.validate_mandatory_parameter('url', url)
        cls.validate_string_parameter('url', url)
        cls.validate_url_is_ok(url)
        # TODO: Validate 'url' file is some FileType

    @classmethod
    def validate_filename(cls, filename: str, file_type: FileType = FileType.IMAGE, is_mandatory: bool = True):
        """
        Validates the 'filename' parameter. If the 'filename' parameter has
        some value, all conditions will be checked. If there is not 'filename'
        and 'is_mandatory' is False, no Exceptions will be raised because it
        is valid.
        """
        if not is_mandatory and not filename:
            return True
        
        cls.validate_mandatory_parameter('filename', filename)
        cls.validate_string_parameter('filename', filename)
        cls.validate_file_exists('filename', filename)
        cls.validate_filename_is_type('filename', filename, file_type)
        # TODO: Validate type trying to instantiate it

    @classmethod
    def validate_rules(cls, rules: Union[AIImageElementRules, ImageElementRules, MemeElementRules, AIVideoElementRules, VideoElementRules, SoundElementRules, CustomStockElementRules, StockElementRules, YoutubeVideoElementRules, TextElementRules, PremadeElementRules]):
        if not isinstance(rules, ElementRules.get_rules_classes()):
            raise Exception(ErrorMessage.parameter_is_not_rules('rules'))
        
    @classmethod
    def validate_builder(cls, builder: Union[ImageElementBuilder, AIImageElementBuilder, VideoElementBuilder, AIVideoElementBuilder, CustomStockElementBuilder, StockElementBuilder, SoundElementBuilder, MemeElementBuilder, YoutubeVideoElementBuilder, TextElementBuilder, PremadeElementBuilder]):
        if not isinstance(builder, ElementBuilder.get_subclasses()):
            raise Exception(f'The provided "builder" parameter is not a valid ElementBuilder subclass. The valid ones are: {', '.join(ElementBuilder.get_subclasses().__str__)}.')