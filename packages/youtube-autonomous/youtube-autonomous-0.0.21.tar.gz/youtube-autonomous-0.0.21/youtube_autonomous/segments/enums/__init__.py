from yta_general_utils.programming.enum import YTAEnum as Enum, get_values


class SegmentType(Enum):
    """
    These Enums represent the types that a Segment could be, allowing
    us to check and detect if it is valid.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
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
    AI_VIDEO = 'ai_video'
    VIDEO = 'video'
    SOUND = 'sound'
    YOUTUBE_VIDEO = 'youtube_video'
    TEXT = 'text'
    MEME = 'meme'
    EFFECT = 'effect'
    PREMADE = 'premade'
    GREENSCREEN = 'greenscreen'

    # TODO: This below is now available through the rules...
    # This should be removed in a near future
    @classmethod
    def get_premade_types(cls):
        """
        Returns a list containing all the Segment Types that are 
        premades.
        """
        return [
            # SegmentType.YOUTUBE_SEARCH,
            # SegmentType.GOOGLE_SEARCH
        ]

    @classmethod
    def get_narration_types(cls):
        """
        Returns the SegmentType enums that are compatible with 
        audio narration.
        """
        return cls.get_all()
    
    @classmethod
    def get_narration_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible
        with audio narration.
        """
        return get_values(cls.get_narration_types())
    
    @classmethod
    def get_url_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'url' parameter.
        """
        return [
            SegmentType.IMAGE,
            SegmentType.YOUTUBE_VIDEO,
            SegmentType.VIDEO,
            SegmentType.SOUND
        ]
    
    @classmethod
    def get_url_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible
        with the 'url' parameter.
        """
        return get_values(cls.get_url_types())
    
    @classmethod
    def get_keywords_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'keywords' parameter.
        """
        return [
            SegmentType.MEME,
            SegmentType.AI_IMAGE,
            SegmentType.CUSTOM_STOCK,
            SegmentType.STOCK,
            # TODO: Add IMAGE in the future with Bing or Google Search
            # TODO: Add YOUTUBE_VIDEO in the future for Youtube Search
        ]
    
    @classmethod
    def get_keywords_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'keywords' parameter.
        """
        return get_values(cls.get_keywords_types())
    
    @classmethod
    def get_filename_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'filename' parameter.
        """
        return [
            SegmentType.IMAGE,
            SegmentType.SOUND,
            SegmentType.VIDEO
        ]
    
    @classmethod
    def get_filename_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'filename' parameter.
        """
        return get_values(cls.get_filename_types())
    
    @classmethod
    def get_text_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'text' parameter.
        """
        # TODO: This is defined in element rules
        return [
            SegmentType.TEXT,
        ]
    
    @classmethod
    def get_text_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'text' parameter.
        """
        return get_values(cls.get_text_types())
    
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
    FILENAME = 'filename'
    NARRATION_TEXT = 'narration_text'
    VOICE = 'voice'
    TEXT = 'text'
    DURATION = 'duration'
    AUDIO_NARRATION_FILENAME = 'audio_narration_filename'
    MUSIC = 'music'

class EnhancementField(Enum):
    """
    Fields accepted for enhancement elements.
    """
    TYPE = 'type'
    KEYWORDS = 'keywords'
    URL = 'url'
    FILENAME = 'filename'
    NARRATION_TEXT = 'narration_text'
    VOICE = 'voice'
    TEXT = 'text'
    AUDION_NARRATION_FILENAME = 'audio_narration_filename'
    MUSIC = 'music'
    START = 'start'
    DURATION = 'duration'
    
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
    GREENSCREEN = 'greenscreen'
    EFFECT = 'effect'
    # TODO: Add more in the future please 'video', 'ai_image', etc.
    # maybe all the segment types
    """
    This enum must be used only for validation process. This has been made to 
    check if some provided type is valid as it is one of the valid and 
    available ones.
    """

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
    
    # TODO: In the future, let this be more personalized
    # NARRATION_TEXT = 'narration_text'
    # VOICE = 'voice'
    # TEXT = 'text'
    # AUDIO_NARRATION_FILENAME = 'audio_narration_filename'
    # MUSIC = 'music'
    #ORIGIN = 'origin'

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
    def get_default(cls):
        return cls.START_OF_FIRST_SHORTCODE_CONTENT_WORD
    
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
    
    @classmethod
    def get_default(cls):
        return cls.SHORTCODE_CONTENT

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
    def get_default(cls):
        """
        Returns the default enum of this list. This value will be used when
        no valid value is found.
        """
        return cls.INLINE

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

class ProjectStatus(Enum):
    """
    The current project status defined by this string.
    """
    TO_START = 'to_start'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'