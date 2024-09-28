from youtube_autonomous.elements.validator import RULES_SUBCLASSES, BUILDER_SUBCLASSES
from yta_general_utils.programming.error_message import ErrorMessage as BaseErrorMessage


class ErrorMessage(BaseErrorMessage):
    @classmethod
    def parameter_is_not_rules(cls, parameter_name: str):
        rules_subclasses_as_str = ', '.join(RULES_SUBCLASSES)
        return f'The provided "{parameter_name}" parameter is not a valid ElementRules subclass. The valid ones are: {rules_subclasses_as_str}.'
    
    @classmethod
    def parameter_is_not_builder(cls, parameter_name: str):
        builder_subclasses_as_str = ', '.join(BUILDER_SUBCLASSES)
        return f'The provided "{parameter_name}" parameter is not a valid ElementBuilder subclass. The valid ones are: {builder_subclasses_as_str}.'