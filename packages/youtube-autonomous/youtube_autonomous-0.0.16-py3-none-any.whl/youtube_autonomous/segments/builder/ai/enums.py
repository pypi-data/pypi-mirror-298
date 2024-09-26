from enum import Enum


class ImageEngine(Enum):
    """
    The engine that is capable of generating AI images.
    """
    PRODIA = 'prodia'
    FLUX = 'flux'
    DEFAULT = PRODIA

class VoiceEngine(Enum):
    """
    The engine that is capable of generation audio voice narrations.
    """
    GOOGLE = 'google'
    MICROSOFT = 'microsoft'
    DEFAULT = GOOGLE
    # TODO: Add more