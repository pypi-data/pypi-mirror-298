from youtube_autonomous.elements.builder.element_builder import ElementBuilder
from youtube_autonomous.elements.rules.element_rules import ElementRules
from yta_general_utils.programming.error_message import ErrorMessage as BaseErrorMessage


class ErrorMessage(BaseErrorMessage):
    @classmethod
    def parameter_is_not_rules(cls, parameter_name: str):
        return f'The provided "{parameter_name}" parameter is not a valid ElementRules subclass. The valid ones are: {', '.join(ElementRules.get_subclasses().__str__)}.'
    
    @classmethod
    def parameter_is_not_builder(cls, parameter_name: str):
        return f'The provided "{parameter_name}" parameter is not a valid ElementBuilder subclass. The valid ones are: {', '.join(ElementBuilder.get_subclasses().__str__)}.'