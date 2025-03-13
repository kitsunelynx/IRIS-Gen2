from core.tools.tool_interface import ToolInterface
from youtubesearchpython import VideosSearch
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeTranscriptTool(ToolInterface):
    def __init__(self):
        self.ctx = None  # this will be set in register()

    @property
    def name(self) -> str:
        return "YoutubeTranscriptTool"

    def register(self, context):
        """
        Store the given limited tool context and return the list of callable functions.
        """
        self.ctx = context
        return [self.fetch_transcript]

    def fetch_transcript(self, video_id: str):
        """
        Fetches the transcript of a YouTube video. Used when user asks to watch the video, meaning to understand the video content. Get the video id from other tools if input in just plain search term.
        If a video_id is provided (or found via query), it will use the YouTubeTranscriptApi to fetch the transcript.

        Returns a dictionary with the complete transcript text, the snippet count, and the last snippet.
        """
        
        if not video_id:
            self.ctx.error("No video_id provided and query was empty.")
            return None

        # Fetch the transcript using the YouTubeTranscriptApi
        try:
            fetched_transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            self.ctx.error(f"Error fetching transcript for video id {video_id}: {e}")
            return None

        transcript_text = ""
        # Iterate over the transcript snippets (each snippet is a dict with a 'text' entry).
        for snippet in fetched_transcript:
            transcript_text += snippet.get("text", "")

        snippet_count = len(fetched_transcript)
        last_snippet = fetched_transcript[-1] if snippet_count > 0 else None
        self.ctx.success(f"Transcript fetched for video id {video_id} with {snippet_count} snippets.")
        return {
            "transcript": transcript_text,
            "snippet_count": snippet_count,
            "last_snippet": last_snippet,
        }

def register():
    """
    This is the module-level register function that the ToolManager will use.
    It creates and returns an instance of the YoutubeTranscriptTool.
    """
    return YoutubeTranscriptTool()