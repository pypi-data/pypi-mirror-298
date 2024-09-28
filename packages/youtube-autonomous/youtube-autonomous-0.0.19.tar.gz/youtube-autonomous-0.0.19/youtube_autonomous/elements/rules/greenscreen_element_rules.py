from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.segments.enums import EnhancementElementMode


class GreenscreenElementRules(ElementRules):
    def __init__(self):
        super().__init__(
            can_have_narration = False,
            need_narration = False,
            can_have_specific_duration = True,
            need_specific_duration = False,
            can_have_text = False,
            need_text = False,
            can_have_filename = True,
            can_have_url = True,
            need_filename_or_url = True,
            can_have_keywords = False,
            need_keywords = False,
            can_have_more_parameters = False,

            can_be_segment = False,
            can_be_enhancement_element = True,
            valid_enhancement_modes = [EnhancementElementMode.REPLACE],
            default_enhancement_mode = EnhancementElementMode.REPLACE
        )