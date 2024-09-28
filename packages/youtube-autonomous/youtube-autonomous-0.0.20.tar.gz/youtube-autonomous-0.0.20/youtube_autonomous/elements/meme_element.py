from youtube_autonomous.elements.rules.meme_element_rules import MemeElementRules
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.segments.enums import SegmentType
from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.elements.rules.rules_checker import RulesChecker
from typing import Union


class ProjectElement:
    @property
    def builder(self):
        return self._builder
    
    @builder.setter
    def builder(self, builder: 'ElementBuilder'):
        ElementParameterValidator.validate_builder(builder)
        
        self._builder = builder

    @property
    def rules(self):
        return self._rules
    
    @rules.setter
    def rules(self, rules: 'ElementRules'):
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

    def __init__(self, type: Union[SegmentType, str]):
        ElementParameterValidator.validate_mandatory_parameter('type', type)
        ElementParameterValidator.validate_is_class('type', type, ['SegmentType', 'str'])
        
        if isinstance(type, str):
            if not SegmentType.is_valid(type):
                raise Exception('The "type" parameter provided is not a valid SegmentType value.')
            
            type = SegmentType(type)

        self.rules = ElementRules.get_subclass_by_type(type)
        self.builder = ElementBuilder.get_subclass_by_type(type)
        self.rules_checker = RulesChecker(self.rules)
    
class MemeElement(ProjectElement):
    def __init__(self):
        super().__init__(SegmentType.MEME)

    def build(self):
        self.builder.build()
