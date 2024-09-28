from youtube_autonomous.segments.builder.youtube.youtube_downloader import YoutubeDownloader
from youtube_autonomous.segments.builder.stock.stock_downloader import StockDownloader
from youtube_autonomous.segments.enums import SegmentType
from youtube_autonomous.segments.builder.config import MAX_DURATION_PER_IMAGE, MIN_DURATION_PER_IMAGE, MAX_DURATION_PER_YOUTUBE_SCENE
from youtube_autonomous.segments.builder.ai import create_ai_image
from yta_multimedia.image.edition.resize import resize_image_scaling
from yta_multimedia.video.dimensions import rescale_video
from yta_multimedia.video.generation import generate_video_from_image
from yta_multimedia.video.generation.google.google_search import GoogleSearch
from yta_multimedia.video.generation.google.youtube_search import YoutubeSearch
from yta_multimedia.video.generation.manim.classes.text.text_word_by_word_manim_animation import TextWordByWordManimAnimation
from yta_general_utils.downloader.image import download_image
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.logger import print_in_progress
from moviepy.editor import VideoFileClip, concatenate_videoclips


class SegmentContentBuilder:
    """
    Class that is able to build the content of a project segment with
    the parameters that are set in the segment.
    """
    def __init__(self):
        # TODO: These objects below are special ones of this project
        # to handle Youtube and Stock elements. I cannot import
        # directly from libraries to use them because it has more
        # logic
        self.youtube_handler = YoutubeDownloader(True)
        self.stock_handler = StockDownloader(True)

    # TODO: Continue
    def build_segment(self, segment):
        """
        Builds a moviepy VideoFileClip based on the provided 'segment'
        properties.
        """
        video = None

        if segment.type == SegmentType.IMAGE.value:
            video = self.__build_image(segment)
        elif segment.type == SegmentType.AI_IMAGE.value:
            video = self.__build_ai_image(segment)
        elif segment.type == SegmentType.CUSTOM_STOCK.value:
            video = self.__build_custom_stock(segment)
        elif segment.type == SegmentType.STOCK.value:
            video = self.__build_stock(segment)
        elif segment.type == SegmentType.YOUTUBE_VIDEO.value:
            video = self.__build_youtube_video(segment)
        elif segment.type == SegmentType.TEXT.value:
            video = self.__build_text_video(segment)
        elif segment.type == SegmentType.MEME.value:
            video = self.__build_meme_video(segment)
        # Accepted premades below
        # TODO: Implement the 'premade' type and the 'subtype' field
        # to manage these kind of premades
        elif segment.type in SegmentType.get_premade_types().values():
            video = self.__build_premade_video(segment)
        else:
            # TODO: This should not happend because of the validator but...
            raise Exception(f'Unexpected segment type "{str(segment.type)}" for content creation.')

        return video

    def __build_image(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType.IMAGE) video and
        returns it as a clip.

        This method will download the image in the 'segment.url' parameter, resize
        it to fit a 1920x1080 screen size, and build the video with a duration of
        'segment.duration' seconds.

        TODO: Review this explanation
        """
        # TODO: We maybe do not need this because of alternative creations which are
        # done when the main type is not available because of any external reason
        # if segment.type != SegmentType.IMAGE:
        #     raise Exception('The given segment is not a SegmentType.IMAGE type.')

        # TODO: Try to do all this process in memory, writting not the image
        image_filename = download_image(segment.url)

        # Resize image to fit the screen
        tmp_image_filename = create_temp_filename(f'image{get_file_extension(image_filename)}')
        resize_image_scaling(image_filename, 1920, 1080, tmp_image_filename)

        # TODO: Apply and Effect (this need work)
        video = generate_video_from_image(tmp_image_filename, segment.calculated_duration, None)

        return video
    
    def __build_ai_image(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType.AI_IMAGE) 
        video and returns it as a clip.

        This method will use the segment keywords to generate one (or more)
        ai images for the moviepy video clip that is returned.
        """
        # We need to know the amount of ai images we need to get the final video
        # because we cannot use only one image for a long time
        # TODO: Implement a 'strategy' field to know if only 1 image or more than
        # one. By now 'more than one' is default
        images = []
        if segment.calculated_duration > MAX_DURATION_PER_IMAGE:
            number_of_images = int(segment.calculated_duration / MAX_DURATION_PER_IMAGE)
            for i in range(number_of_images):
                images.append({
                    'keywords': segment.keywords,
                    'duration': MAX_DURATION_PER_IMAGE
                })

            remaining_duration = segment.calculated_duration % MAX_DURATION_PER_IMAGE
            if remaining_duration <= MIN_DURATION_PER_IMAGE:
                # We won't create an image animation that is too short, we
                # will make the previous one longer
                images[len(images) - 1]['duration'] += remaining_duration
            else:
                images.append({
                    'keywords': segment.keywords,
                    'duration': remaining_duration
                })
        else:
            images.append({
                'keywords': segment.keywords,
                'duration': segment.calculated_duration
            })

        # Let's build the final video
        videos = []
        for image in images:
            image_filename = create_ai_image(image.keywords)
            # Resize image to fit the screen
            tmp_image_filename = create_temp_filename(f'image{get_file_extension(image_filename)}')
            resize_image_scaling(image_filename, 1920, 1080, tmp_image_filename)

            # TODO: Apply and Effect (this need work)
            videos.append(generate_video_from_image(tmp_image_filename, image.duration, None))

        video = concatenate_videoclips(videos)

        return video

    def __build_custom_stock(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType.CUSTOM_STOCK) 
        video and returns it as a clip.

        This method will use the segment keywords to look for custom stock
        videos for the moviepy video clip that is returned.
        """
        videos = []
        do_use_youtube = True # to stop searching in Youtube if no videos available
        accumulated_duration = 0
        while accumulated_duration < segment.calculated_duration:
            downloaded_filename = None
            if do_use_youtube:
                # We try to download if from Youtube
                print_in_progress('Downloading youtube stock video')
                youtube_stock_video = self.youtube_handler.get_stock_video(segment.keywords)
                if youtube_stock_video:
                    downloaded_filename = youtube_stock_video.download_with_audio(output_filename = create_temp_filename('youtube.mp4'))
                    if downloaded_filename:
                        self.youtube_handler.add_ignored_id(youtube_stock_video.id)

            if not downloaded_filename:
                # Not found or not searching on Youtube, so build 'stock'
                print_in_progress('Downloading stock video (youtube not found)')
                do_use_youtube = False
                video = self.build_stock_video_content_clip_from_segment(segment)
            else:
                video = VideoFileClip(downloaded_filename)

            accumulated_duration += video.duration

            if accumulated_duration > segment.calculated_duration:
                end = video.duration - (accumulated_duration - segment.calculated_duration)
                start = 0
                if youtube_stock_video:
                    if youtube_stock_video.key_moment != 0:
                        # Ok, lets use that key moment as the center of our video
                        start = youtube_stock_video.key_moment - (end / 2)
                        end = youtube_stock_video.key_moment + (end / 2)
                        if start < 0:
                            end += abs(0 - start)
                            start = 0
                        if end > video.duration:
                            start -= abs(end - video.duration)
                            end = video.duration
                    video = video.subclip(start, end)
                else:
                    video = video.subclip(start, end)

            videos.append(video)

        return concatenate_videoclips(videos)
    
    def __build_stock(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType.STOCK) 
        video and returns it as a clip.

        This method will use the segment keywords to look for stock videos 
        for the moviepy video clip that is returned.
        """
        videos = []
        accumulated_duration = 0
        while accumulated_duration < segment.calculated_duration:
            print_in_progress('Downloading stock video')
            # TODO: Make this force 1920x1080 resolution
            downloaded_filename = self.stock_handler.download_video(segment.keywords, True)

            if not downloaded_filename:
                # No stock videos available, lets build with AI
                video = self.__build_ai_image(segment)
            else:
                video = rescale_video(downloaded_filename)
                # TODO: Maybe 'resize_video' instead of 'rescale_video' (?)

            accumulated_duration += video.duration
            # Last clip must be cropped to fit the expected duration
            if accumulated_duration > segment.calculated_duration:
                video = video.subclip(0, video.duration - (accumulated_duration - segment.calculated_duration))
            # TODO: I'm forcing 1920, 1080 here but it must come from Pexels
            videos.append(video)

        return concatenate_videoclips(videos)

    # TODO: This method should be refactored as it is not worth I think
    def __build_youtube_video(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType.YOUTUBE_VIDEO) 
        video and returns it as a clip.

        This method will use the segment url to look for that Youtube video and
        make a custom moviepy video clip that is returned.
        """
        # TODO: This functionality must go to 'yta_multimedia' or, at
        # least, to 'youtube_handler' because I will have different
        # strategies to build segment videos from Youtube videos so I
        # need this method clean to choose a method according to the 
        # strategy without too much code here :)

        # Get the youtube video
        youtube_video = self.youtube_handler.get_video(segment.url)

        if not youtube_video.is_available():
            raise Exception('The youtube video with url "' + str(segment.url) + '" is not available.')

        scenes_number = segment.calculated_duration / MAX_DURATION_PER_YOUTUBE_SCENE
        if (segment.calculated_duration + MAX_DURATION_PER_YOUTUBE_SCENE) > 0:
            scenes_number += 1
        scene_duration = segment.calculated_duration / scenes_number

        youtube_video_scenes = []
        if youtube_video.heatmap:
            youtube_video_scenes = youtube_video.get_hottest_scenes(scenes_number, scene_duration)
        else:
            youtube_video_scenes = youtube_video.get_scenes(scenes_number, scene_duration)

        # Now we have all scenes, subclip the youtube clip
        youtube_clip = VideoFileClip(self.youtube_handler.download_this_video(youtube_video))
        scene_clips = []
        for scene in youtube_video_scenes:
            scene_clips.append(youtube_clip.subclip(scene['start'], scene['end']))

        return concatenate_videoclips(scene_clips)
    
    def __build_text_video(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType.TEXT) 
        video and returns it as a clip.

        This method will use the segment text create a custom text animation 
        moviepy video clip that is returned.
        """
        # TODO: I need to add new fields like 'strategy', 'subtype', 'background'
        # or things that make me being able to customize the text video creation
        # and later, if they are not provided, just randomize them in code but
        # from a wide group of options
        
        # TODO: We need to check if this text must be build from the transcription
        # or if it is a plain text with a whole and specific duration, with or 
        # without audio... Little more complex than previous ones
        temp_filename = create_temp_filename('manim.mp4')
        # OPTIONS BELOW
        if segment.audio_narration_filename:
            # Text without duration but it has audio narration file
            duration = segment.audio_clip.duration
            transcription = segment.transcription
            # TODO: We need a strategy to build this

            # TODO: Please, document what does whisper returns inside
            # the object and in 'transcription' property in 'segment.py'
            # file to not forget it
            print(transcription)
            
            # TODO: This is just to test, use one synchronized with 
            # transcription
            text = ' '.join(d['word'] for d in transcription)
            temp_filename = TextWordByWordManimAnimation().generate(text, duration, temp_filename)
        # Text without duration but its narrated by system
        elif segment.text and segment.voice:
            duration = segment.audio_clip.duration
            transcription = segment.transcription
            # TODO: We need a strategy to build this

            # TODO: This is just to test, use one synchronized with 
            # transcription
            text = ' '.join(d['word'] for d in transcription)
            temp_filename = TextWordByWordManimAnimation().generate(text, duration, temp_filename)
        else:
            if not segment.text:
                raise Exception('No "text" in segment to be able to build the text video.')
            
            # TODO: I think any other option is avoided by the validator, but
            # confirm it and remove this comment then
            
            # Text with duration (and music maybe) but no narration
            duration = segment.duration
            text = segment.text
            # TODO: We need a strategy to build this

            temp_filename = TextWordByWordManimAnimation().generate(text, duration, temp_filename)
        
        return VideoFileClip(temp_filename)
    
    def __build_meme_video(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType.MEME) video 
        and returns it as a clip.

        This method will use the segment keywords for a custom meme to create 
        the moviepy video clip that is returned.
        """
        self.youtube_handler.deactivate_ignore_repeated()
        temp_filename = self.youtube_handler.download_meme_video(segment.keywords, True, True)
        self.youtube_handler.activate_ignore_repeated()

        # TODO: Look for a better strategy (?)
        if not temp_filename:
            raise Exception('No meme found with the given "keywords": ' + str(segment.keywords) + '.')
        

        return VideoFileClip(temp_filename)
    
    def __build_premade_video(self, segment):
        """
        Builds the provided 'segment' (that must be a SegmentType of a premade) 
        video and returns it as a clip.

        This method will use the segment parameters to build a custom premade 
        moviepy video clip that is returned.
        """
        video = None

        if segment.type == SegmentType.GOOGLE_SEARCH.value:
            video = GoogleSearch(self.keywords).generate()
        elif segment.type == SegmentType.YOUTUBE_SEARCH.value:
            video = YoutubeSearch(self.keywords).generate()

        return video
