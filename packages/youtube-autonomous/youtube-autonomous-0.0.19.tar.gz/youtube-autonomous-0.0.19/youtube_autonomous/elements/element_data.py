#from youtube_autonomous.segments.enums import SegmentField


class ElementData:
    """
    A class to handle any project Element information.
    """
    # Narration
    audio_narration_filename: str
    narration_text: str
    voice: str
    # Text
    text: str
    # Specific duration
    duration: float
    # Source (filename or url)
    filename: str
    url: str
    # Source or identifier (keywords)
    keywords: str

    # During building
    calculated_duration: float
    start: float
    mode: str
    audio_filename: str
    video_filename: str
    full_filename: str
    transcription = None
    shortcodes = []

    def __init__(self, json: dict):
        # TODO: Apply 'SegmentField' instead of this strings, please
        self.audio_narration_filename = json.get('audio_narration_filename', '')
        self.narration_text = json.get('narration_text', '')
        self.voice = json.get('voice', '')

        self.text = json.get('text', '')

        self.duration = json.get('duration', None)
        
        self.filename = json.get('filename', '')
        self.url = json.get('url', '')

        self.keywords = json.get('keywords', '')

        self.calculated_duration = json.get('calculated_duration', None)
        self.start = json.get('start', None)
        self.mode = json.get('mode', '')
        self.audio_filename = json.get('audio_filename', '')
        self.video_filename = json.get('video_filename', '')
        self.full_filename = json.get('full_filename', '')

    def as_enum(self):
        """
        Returns the information
        """
        # TODO: (?)