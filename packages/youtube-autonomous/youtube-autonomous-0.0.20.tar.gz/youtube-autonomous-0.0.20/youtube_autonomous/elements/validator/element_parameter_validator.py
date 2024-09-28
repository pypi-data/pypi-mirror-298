
from youtube_autonomous.elements.validator.error_message import ErrorMessage
from youtube_autonomous.segments.enums import SegmentType
from youtube_autonomous.elements.validator import RULES_SUBCLASSES, BUILDER_SUBCLASSES
from yta_general_utils.programming.parameter_validator import ParameterValidator
from yta_general_utils.file.filename import FileType
from typing import Union


class ElementParameterValidator(ParameterValidator):
    """
    A validator that will raise an Exception if any of the used
    checkings is invalid, or will return the value if ok.
    """
    @classmethod
    def validate_keywords(cls, keywords: str):
        cls.validate_string_mandatory_parameter('keywords', keywords)

        return keywords

    @classmethod
    def validate_text(cls, text: str):
        cls.validate_string_mandatory_parameter('text', text)

        return text
    
    @classmethod
    def validate_premade_name(cls, premade_name: str):
        cls.validate_string_mandatory_parameter('premade_name', premade_name)
        # TODO: Maybe validate that is a key of a valid premade (?)

        return premade_name
    
    @classmethod
    def validate_text_class_name(cls, text_class_name: str):
        cls.validate_string_mandatory_parameter('text_class_name', text_class_name)
        # TODO: Maybe validate that is a key of a valid text_class (?)

        return text_class_name
    
    @classmethod
    def validate_duration(cls, duration: Union[int, float]):
        # TODO: Maybe validate that is a key of a valid text class (?)
        cls.validate_numeric_positive_mandatory_parameter('duration', duration)

        return duration
    
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

        return url

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

        return filename

    @classmethod
    def validate_rules(cls, rules: 'ElementRules'):
        if not type(rules).__name__ in RULES_SUBCLASSES:
            raise Exception(ErrorMessage.parameter_is_not_rules('rules'))
        
        return rules
        
    @classmethod
    def validate_builder(cls, builder: 'ElementBuilder'):
        if not type(builder).__name__ in BUILDER_SUBCLASSES:
            raise Exception(ErrorMessage.parameter_is_not_builder('builder'))
        
        return builder
        
    @classmethod
    def validate_segment_type(cls, type: Union[SegmentType, str]):
        cls.validate_mandatory_parameter('type', type)
        cls.validate_is_class('type', type, ['SegmentType', 'str'])

        if isinstance(type, str):
            if not SegmentType.is_valid(type):
                raise Exception('The "type" parameter provided is not a valid SegmentType value.')
            
            type = SegmentType(type)

        return type