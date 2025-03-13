from youtubesearchpython import VideosSearch
from core.tools.tool_interface import ToolInterface

class ExtractYoutubeVideoIDTool(ToolInterface):
    @property
    def name(self) -> str:
        return "ExtractYoutubeVideoIDTool"

   

    def register(self, context) -> list:
        """
        Registers the tool with the provided ToolContext.
        This method logs the registration process and returns a list with a callable that
        runs the extract_video_id function.
        """
        context.debug("Registering ExtractYoutubeVideoIDTool.")
        
        def extract_youtube_video_id(query: str) -> str:
            """
            Search YouTube for the given query and return the id of the first video found. Can be used to play videos in frontend.
            
            Parameters:
            - query: The search term (default is "Back in black").
            
            Returns:
            - The id of the first video result, or an empty string if no result is found.
            """
            context.info(f"Extracting YouTube video ID for query: {query}")
            videos_search = VideosSearch(query)
            results = videos_search.result()
            
            if "result" in results and len(results["result"]) > 0:
                return results["result"][0]["id"]
            
            return ""
        
        return [extract_youtube_video_id]

def register():
    """
    This top-level register function is used by the tool manager to load the tool.
    """
    return ExtractYoutubeVideoIDTool()
