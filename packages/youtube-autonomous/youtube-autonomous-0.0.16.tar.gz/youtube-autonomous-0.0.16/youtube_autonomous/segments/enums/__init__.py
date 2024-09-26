from yta_general_utils.programming.enum import is_valid, get_all
from enum import Enum


# TODO: Add all 'is_valid' and 'get_all' methods
class SegmentType(Enum):
    """
    These Enums represent the types that a Segment could be, allowing
    us to check and detect if it is valid.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    # TODO: Remove 'MY_STOCK' when refactored (now use CUSTOM_STOCK)
    MY_STOCK = 'my_stock'
    CUSTOM_STOCK = 'custom_stock'
    """
    Stock videos but extracted from our own custom sources.
    """
    STOCK = 'stock'
    """
    Stock videos extracted from external stock platforms.
    """
    AI_IMAGE = 'ai_image'
    IMAGE = 'image'
    YOUTUBE_VIDEO = 'youtube_video'
    YOUTUBE_SEARCH = 'youtube_search'
    GOOGLE_SEARCH = 'google_search'
    TEXT = 'text'
    MEME = 'meme'

    @classmethod
    def get_premade_types(cls):
        """
        Returns a list containing all the Segment Types thar are 
        premades.
        """
        return [SegmentType.YOUTUBE_SEARCH, SegmentType.GOOGLE_SEARCH]

    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid SegmentType 
        enum value, or False if not.
        """
        return is_valid(value, SegmentType)
    
class SegmentField(Enum):
    """
    These Enums represent the fields that a Segment has, allowing us
    to check that any required field is provided and/or to detect 
    which one is missing.

    Examples: TYPE, KEYWORDS, URL, etc.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    TYPE = 'type'
    KEYWORDS = 'keywords'
    URL = 'url'
    TEXT = 'text'
    VOICE = 'voice'
    DURATION = 'duration'
    AUDIO_NARRATION_FILENAME = 'audio_narration_filename'
    
    @classmethod
    def get_all(cls):
        """
        Returns a list containing all the registered SegmentField enums.
        """
        return get_all(SegmentField)
    
    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid SegmentField 
        enum value, or False if not.
        """
        return is_valid(value, SegmentField)
    
class SegmentBuildingField(Enum):
    """
    The fields that are used when building the segment and are
    not provided by the user in the initial segment json data.
    """
    TRANSCRIPTION = 'transcription'
    AUDIO_FILENAME = 'audio_filename'
    AUDIO_CLIP = 'audio_clip'
    VIDEO_FILENAME = 'video_filename'
    VIDEO_CLIP = 'video_clip'
    FULL_FILENAME = 'full_filename'
    FULL_CLIP = 'full_clip'
    # TODO: What about 'status', 'music_filename' and any other (if existing) (?)

class ProjectField(Enum):
    """
    The fields that are used to handle the project information.
    """
    STATUS = 'status'
    """
    The current status of the project, that must be a ProjectStatus
    enum.
    """
    SEGMENTS = 'segments'
    """
    The array that contains all the information about each one of 
    his segments.
    """

class EnhancementElementType(Enum):
    """
    These Enums represent the type of elements we can use to enhance
    a segment.
    """
    MEME = 'meme'
    STICKER = 'sticker'
    IMAGE = 'image'
    SOUND = 'sound'
    GREEN_SCREEN = 'green-scren'
    EFFECT = 'effect'
    """
    This enum must be used only for validation process. This has been made to 
    check if some provided type is valid as it is one of the valid and 
    available ones.
    """
    @classmethod
    def get_all(cls):
        """
        Returns a list containing all the registered EnhancementElementType
        enums.
        """
        return get_all(EnhancementElementType)
    
    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid EnhancementElementType 
        enum value, or False if not.
        """
        return is_valid(value, EnhancementElementType)

class EnhancementElementField(Enum):
    """
    These Enums represent the type of fields we can use with the
    segment enhancement elements to fit correctly the segment.
    """
    # IS_ACTIVE = 'is_active'
    # """
    # This field determines if the current enhancement element is active or not,
    # allowing us to have the information but applying not this element for an
    # specific segment.
    # """
    START = 'start'
    """
    This field determines the time moment (related to the segment video time)
    in which the enhancement element should start, expressed in seconds. This
    can be a number or an EnhancementElementStart enum.
    """
    DURATION = 'duration'
    """
    This field determines the time that the enhancement element should last 
    since the 'start' moment, expressed in seconds. This can be a number or
    an EnhancementElementDuration enum.
    """
    KEYWORDS = 'keywords'
    FILENAME = 'filename'
    URL = 'url'
    MODE = 'mode'
    #ORIGIN = 'origin'

    @classmethod
    def get_all(cls):
        """
        Returns a list containing all the registered EnhancementElementField
        enums.
        """
        return get_all(EnhancementElementField)
    
    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid EnhancementElementField 
        enum value, or False if not.
        """
        return is_valid(type, value)
    


class EnhancementElementStart(Enum):
    """
    These Enums are valid values for the 'start' EnhancementElementField.
    """
    BETWEEN_WORDS = 'between_words'
    """
    This will make the enhancement element start just in the middle of 
    two words that are dictated in narration. This means, after the end
    of the first and and before the start of the next one (that should
    fit a silence part).
    """
    START_OF_FIRST_SHORTCODE_CONTENT_WORD = 'start_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content starts being dictated.
    """
    MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD = 'middle_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content is in the middle of the dictation.
    """
    END_OF_FIRST_SHORTCODE_CONTENT_WORD = 'end_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content ends being dictated.
    """
    
    @classmethod
    def get_all(cls):
        """
        Returns a list containing all the registered EnhancementElementStart
        enums.
        """
        return get_all(EnhancementElementStart)
    
    @classmethod
    def get_all_values(cls):
        """
        Returns a list containing all the registered EnhancementElementStart
        enum values.
        """
        return [item.value for item in get_all()]
    
    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid EnhancementElementStart 
        enum value, or False if not.
        """
        return is_valid(type, value)
    
class EnhancementElementDuration(Enum):
    """
    These Enums represent the time, during a segment lifetime, that
    the elements are going to last (be shown).
    """
    SHORTCODE_CONTENT = 'shortcode_content'
    """
    This will make the enhancement element last until the shortcode
    block-scoped content is narrated.
    """
    FILE_DURATION = 'file_duration'
    """
    This will make the segment last the clip duration. It will be
    considered when the file is downloaded, and that duration will
    be flagged as 9999. This is for videos or audios that have a
    duration based on file.
    """
    DEFAULT = SHORTCODE_CONTENT

    @classmethod
    def get_all(cls):
        """
        Returns a list containing all the registered EnhancementElementDuration
        enums.
        """
        return get_all(EnhancementElementDuration)
    
    @classmethod
    def get_all_values(cls):
        """
        Returns a list containing all the registered EnhancementElementDuration
        enum values.
        """
        return [item.value for item in get_all()]
    
    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid EnhancementElementDuration 
        enum value, or False if not.
        """
        return is_valid(type, value)
    
class EnhancementElementMode(Enum):
    """
    These Enums represent the different ways in which the project
    segment elements can be built according to the way they are
    included in the segment.
    """
    INLINE = 'inline'
    """
    Those segment elements that will be displayed in 'inline' mode, that
    means they will interrupt the main video, be played, and then go back
    to the main video. This will modify the clip length, so we need to 
    refresh the other objects start times.
    """
    OVERLAY = 'overlay'
    """
    Those segment elements that will be displayed in 'overlay' mode, that
    means they will be shown in the foreground of the main clip, changing
    not the main video duration, so they don't force to do any refresh.
    """
    REPLACE = 'replace'
    """
    Those enhancement elements that will replace the video in this mode.
    This means that the original video is modified by this enhancement
    element and that modified part will be placed instead of the original
    video. This modified part could be the whole video or only a part of
    it. This is how most of the greenscreens or effects are applied.
    """
    
    @classmethod
    def get_all(cls):
        """
        Returns a list containing all the registered EnhancementElementMode
        enums.
        """
        return get_all(EnhancementElementMode)
    
    @classmethod
    def get_all_values(cls):
        """
        Returns a list containing all the registered EnhancementElementMode
        enum values.
        """
        return [item.value for item in get_all()]

    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid EnhancementElementMode 
        enum value, or False if not.
        """
        return is_valid(type, value)
    
    @classmethod
    def default(cls):
        """
        Returns the default enum of this list. This value will be used when
        no valid value is found.
        """
        return EnhancementElementMode.INLINE

class SegmentConstants(Enum):
    """
    These Enums are constants we need to use during the project
    and segments processing.
    """
    FILE_DURATION = 9999
    """
    This is the duration, as int value, that will be considered as
    the original video duration and will be used to set the original
    clip (that can be downloaded or load from local storage) duration
    as the final duration. This amount is just to be recognized and 
    will be replaced, when file processed, by the real duration.
    """



class SegmentElementOrigin(Enum): 
    """
    These Enums represent the way in which the project segment elements
    are searched and obtained from.
    """   
    YOUTUBE = 'youtube'
    """
    Those segment elements that will be searched in Youtube and downloaded
    if found and available.
    """
    FILE = 'file'
    """
    Those segment elements that will be load from local storage. The 
    location must be set in the segment building object.
    """
    DEFAULT = YOUTUBE
    """
    This is the default value I want (me, the developer, is the one who
    sets it by now). This one will be pointing to another of the available
    Enums. This Enum has been created to make it easy building objects in
    code and having the default value in only one strict place.
    """
    ALL = [YOUTUBE, FILE]
    """
    This is for validation purposes only.
    """

class SegmentStatus(Enum):
    """
    The current segment status defined by this string.
    """
    TO_START = 'to_start'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'

    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid SegmentStatus enum
        value,
        or False if not.
        """
        return is_valid(value, SegmentStatus)
    
    @classmethod
    def get_all(cls):
        return get_all(SegmentStatus)

class ProjectStatus(Enum):
    """
    The current project status defined by this string.
    """
    TO_START = 'to_start'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'

    @classmethod
    def is_valid(cls, value: str):
        """
        Returns True if the provided 'value' is a valid ProjectStatus enum
        value, or False if not.
        """
        return is_valid(value, ProjectStatus)
        

