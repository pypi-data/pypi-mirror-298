from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.segments.enums import EnhancementElementMode


class StockElementRules(ElementRules):
    def __init__(self):
        super().__init__(
            can_have_narration = True,
            need_narration = False,
            can_have_specific_duration = True,
            need_specific_duration = False,
            can_have_text = False,
            need_text = False,
            can_have_filename = False,
            can_have_url = False,
            need_filename_or_url = False,
            can_have_keywords = True,
            need_keywords = True,
            can_have_more_parameters = False,

            can_be_segment = True,
            can_be_enhancement_element = True,
            valid_enhancement_modes = [EnhancementElementMode.INLINE, EnhancementElementMode.OVERLAY],
            default_enhancement_mode = EnhancementElementMode.OVERLAY
        )