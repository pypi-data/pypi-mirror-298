from youtube_autonomous.segments.enhancement.edition_manual.edition_manual_term import EditionManualTerm
from typing import Union


class EditionManual:
    @property
    def terms(self):
        return self._terms
    
    @terms.setter
    def terms(self, terms: list[EditionManualTerm]):
        if not terms:
            terms = []

        if any(not isinstance(term, EditionManualTerm) for term in terms):
            raise Exception('At least one of the provided "terms" is not an EditionManualTerm.')

        self._terms = terms

    def __init__(self, terms: Union[list[dict], list[EditionManualTerm]]):
        # TODO: We need an ID or something maybe
        self.terms = terms