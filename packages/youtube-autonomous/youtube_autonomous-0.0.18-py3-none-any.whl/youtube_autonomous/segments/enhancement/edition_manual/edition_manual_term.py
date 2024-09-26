from youtube_autonomous.segments.enhancement.edition_manual.enums import EditionManualTermMode, EditionManualTermContext
from youtube_autonomous.segments.enums import EnhancementElementStart, EnhancementElementDuration
from youtube_autonomous.segments.enhancement.enhancement_element import EnhancementElement
from typing import Union


class EditionManualTerm:
    """
    A term of the edition manual terms book that is used to look
    for matches in the segments text in order to enhance the video
    or audio content.

    See: https://www.notion.so/Diccionarios-de-mejora-155efcba8f0d44e0890b178effb3be84?pvs=4
    """
    @property
    def term(self):
        # TODO: Explain the term
        return self._term
    
    @term.setter
    def term(self, term: str):
        if not term:
            raise Exception('no "term" provided.')
        
        if not isinstance(term, str):
            raise Exception('The "term" parameter provided is not a string.')
        
        self._term = term

    @property
    def mode(self):
        # TODO: Explain the term
        return self._mode
        
    @mode.setter
    def mode(self, mode: Union[EditionManualTermMode, str]):
        if not mode:
            raise Exception('No "mode" provided.')
        
        if not isinstance(mode, (EditionManualTermMode, str)):
            raise Exception('The "mode" parameter provided is not a valid EditionManualTermMode nor a string.')
        
        if isinstance(mode, str):
            if not EditionManualTermMode.is_valid(mode):
                raise Exception('The "mode" parameter provided is not a valid EditionManualTermMode value.')
            
            mode = EditionManualTermMode(mode)

        self._mode = mode

    @property
    def context(self):
        # TODO: Explain the term
        return self._context
    
    @context.setter
    def context(self, context: Union[EditionManualTermContext, str]):
        if not context:
            raise Exception('No "context" provided.')
        
        if not isinstance(context, (EditionManualTermContext, str)):
            raise Exception('The "context" parameter provided is not a valid EditionManualTermContext nor a string.')
        
        if isinstance(context, str):
            if not EditionManualTermContext.is_valid(context):
                raise Exception('The "context" parameter provided is not a valid EditionManualTermContext value.')
            
            context = EditionManualTermContext(context)

        self._context = context

    @property
    def enhancements(self):
        return self._enhancements
    
    @enhancements.setter
    def enhancements(self, enhancements: list[EnhancementElement, dict]):
        # TODO: Make some checkings and improvements
        if not enhancements:
            enhancements = []

        # We turn dicts to EnhancementElement if necessary
        obj_enhancements = []
        for enhancement in enhancements:
            if not isinstance(enhancement, EnhancementElement) and not issubclass(enhancement, EnhancementElement):
                obj_enhancements.append(EnhancementElement.get_class_from_type(enhancement['type'])(enhancement['type'], EnhancementElementStart.START_OF_FIRST_SHORTCODE_CONTENT_WORD, EnhancementElementDuration.SHORTCODE_CONTENT, enhancement['keywords'], enhancement.get('url', ''), enhancement.get('filename', ''), enhancement['mode']))
            else:
                obj_enhancements.append(enhancement)

        self._enhancements = obj_enhancements

    def __init__(self, term: str, mode: str, context: str, enhancements: list[dict]):
        self.term = term
        self.mode = mode
        self.context = context
        self.enhancements = enhancements