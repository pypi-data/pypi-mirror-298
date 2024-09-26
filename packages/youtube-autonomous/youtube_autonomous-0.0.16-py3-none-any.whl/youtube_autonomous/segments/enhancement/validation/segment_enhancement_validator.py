from youtube_autonomous.segments.enums import EnhancementElementField, EnhancementElementType, EnhancementElementDuration, EnhancementElementStart, EnhancementElementMode
from youtube_autonomous.segments.enhancement.enhancement_element import EnhancementElement
from yta_general_utils.checker.type import variable_is_positive_number


class SegmentEnhancementValidator:
    """
    This class is to validate the Segment enhancement elements that
    are terms that the user register to enhance (to improve) the
    project video experience.

    These terms need to have a valid structure and that's what we
    check here.
    """
    def is_valid(enhancement_terms):
        """
        We will receive the content of a enhancement term and will raise an
        Exception if some structure element or value is not valid according
        to our rules.

        TODO: Write a little bit more about what we are receiving here.
        """
        # TODO: Maybe refactor the terms to simplify them
        for enhancement_term_key in enhancement_terms:
            enhancement_term = enhancement_terms[enhancement_term_key]
            for type in enhancement_term:
                content = enhancement_term[type]
                if not EnhancementElementType.is_valid(type):
                    raise Exception('Enhancement element type "' + type + '" not accepted.')

                # Lets check values
                keywords = content.get(EnhancementElementField.KEYWORDS.value)
                filename = content.get(EnhancementElementField.FILENAME.value)
                url = content.get(EnhancementElementField.URL.value)
                start = content.get(EnhancementElementField.START.value)
                mode = content.get(EnhancementElementField.MODE.value)
                duration = content.get(EnhancementElementField.DURATION.value)

                if not keywords and not filename and not url:
                    raise Exception('No "keywords" nor "filename" nor "url" provided.')
                
                # TODO: Search for the element with 'keywords' to check that it
                # doesn't exist (or it does)
                # TODO: Check that provided 'filename' is a valid file and the
                # type is appropriate for the type
                # TODO: Check that the provided 'url' is valid, available and
                # suitable for the type we want
                
                if type == EnhancementElementType.MEME.value and not keywords:
                    raise Exception(f'No "keywords" provided when necessary for the "{EnhancementElementType.MEME.value}" type.')

                start_values = EnhancementElementStart.get_all_values()
                if start and start not in start_values and not variable_is_positive_number(start):
                    raise Exception(f'No valid "start" value provided. Must be one of these "{', '.join(start_values)}" or a valid positive number (including 0).')

                duration_values = EnhancementElementDuration.get_all_values()
                if duration and duration not in duration_values and not variable_is_positive_number(duration):
                    raise Exception(f'No valid "duration" value provided. Must be one of these "{', '.join(duration_values)}" or a valid positive number (including 0).')

                mode_values = EnhancementElementMode.get_all_values()
                if mode and mode not in mode_values:
                    raise Exception(f'No valid "mode" value provided. Must be one of these "{', '.join(mode_values)}".')
                
                