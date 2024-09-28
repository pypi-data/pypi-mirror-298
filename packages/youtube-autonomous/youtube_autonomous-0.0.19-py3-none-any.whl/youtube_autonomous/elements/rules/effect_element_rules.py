from youtube_autonomous.elements.rules.element_rules import ElementRules
from youtube_autonomous.segments.enums import EnhancementElementMode


class EffectElementRules(ElementRules):
    def __init__(self):
        super().__init__(
            can_have_narration = False,
            need_narration = False,
            can_have_specific_duration = False,
            need_specific_duration = False,
            can_have_text = False,
            need_text = False,
            can_have_filename = False,
            can_have_url = False,
            need_filename_or_url = False,
            can_have_keywords = True,
            need_keywords = True,
            can_have_more_parameters = True,
            # TODO: The effect should have some way to detect the
            # mandatory parameters so we can dynamically raise an
            # Exception if any of those mandatory parameters are
            # not provided

            can_be_segment = False,
            can_be_enhancement_element = True,
            valid_enhancement_modes = [EnhancementElementMode.REPLACE],
            default_enhancement_mode = EnhancementElementMode.REPLACE
        )