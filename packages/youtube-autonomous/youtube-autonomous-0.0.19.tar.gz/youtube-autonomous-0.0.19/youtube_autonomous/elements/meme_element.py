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
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
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
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from typing import Union


class ProjectElement:
    @property
    def builder(self):
        return self._builder
    
    @builder.setter
    def builder(self, builder: Union[ImageElementBuilder, AIImageElementBuilder, VideoElementBuilder, AIVideoElementBuilder, CustomStockElementBuilder, StockElementBuilder, SoundElementBuilder, MemeElementBuilder, YoutubeVideoElementBuilder, TextElementBuilder, PremadeElementBuilder]):
        ElementParameterValidator.validate_builder(builder)
        
        self._builder = builder

    @property
    def rules(self):
        return self._rules
    
    @rules.setter
    def rules(self, rules: Union[AIImageElementRules, ImageElementRules, MemeElementRules, AIVideoElementRules, VideoElementRules, SoundElementRules, CustomStockElementRules, StockElementRules, YoutubeVideoElementRules, TextElementRules, PremadeElementRules]):
        ElementParameterValidator.validate_rules(rules)

        self._rules = rules

    @property
    def rules_checker(self):
        return self._rules_checker
    
    @rules_checker.setter
    def rules_checker(self, rules_checker: RulesChecker):
        # TODO: move this to 'ElementParameterValidator'
        if not isinstance(rules_checker, RulesChecker):
            raise Exception(f'The provided "rules_checker" parameter is not one of the following instances: {", ".join([RulesChecker.__str__])}')
        
        self._rules_checker = rules_checker

    def __init__(self, rules: Union[AIImageElementRules, ImageElementRules, MemeElementRules, AIVideoElementRules, VideoElementRules, SoundElementRules, CustomStockElementRules, StockElementRules, YoutubeVideoElementRules, TextElementRules, PremadeElementRules], builder: Union[ImageElementBuilder, AIImageElementBuilder, VideoElementBuilder, AIVideoElementBuilder, CustomStockElementBuilder, StockElementBuilder, SoundElementBuilder, MemeElementBuilder, YoutubeVideoElementBuilder, TextElementBuilder, PremadeElementBuilder]):
        self.rules = rules
        self.builder = builder
        self.rules_checker = RulesChecker(rules)

        # TODO: Add 'segment' but less strict (?)
    
class MemeElement(ProjectElement):
    def __init__(self):
        super().__init__(rules = MemeElementRules, builder = MemeElementBuilder)

    def build(self):
        self.builder.build()
