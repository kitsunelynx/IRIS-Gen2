"""
WebSearchTool - A tool for performing web searches using DuckDuckGo and our custom search implementation.
This tool implements the ToolInterface and registers a 'websearch' function that queries DuckDuckGo,
fetches the content from resulting URLs, and returns an aggregated text.
"""

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from core.utils.logger import get_logger
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
from typing import List, Callable
from core.tools.tool_interface import ToolInterface  # Refactored naming
from core.tools.tool_context import ToolContext      # Refactored naming

class WebSearch:
    def __init__(self, max_results=7, concurrency=5):
        """
        Initialize WebSearch with configurable parameters.
        """
        self.logger = get_logger()
        self.max_results = max_results
        self.headers = {'User-Agent': 'MyWebSearchBot/1.0'}
        
        # Set parser: prefer lxml for speed, fallback to html.parser
        try:
            import lxml
            self.parser = "lxml"
        except ImportError:
            self.parser = "html.parser"
            self.logger.warning("lxml not installed; falling back to html.parser (slower)")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        before_sleep=before_sleep_log(get_logger(), logging.WARNING)
    )
    def fetch_url(self, url: str) -> tuple:
        """
        Fetch URL content with retries and error handling synchronously.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            if response.status_code == 200:
                text = response.text
                soup = BeautifulSoup(text, self.parser)
                page_text = soup.get_text(separator=" ", strip=True)
                return url, page_text
            else:
                return url, f"HTTP Error: {response.status_code}"
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return url, f"Error: {e}"

    def search(self, query: str) -> str:
        """
        Perform a synchronous DuckDuckGo search and fetch content.
        """
        self.logger.info(f"Starting web search for query: {query}")
        try:
            search_results = list(DDGS().text(query, max_results=self.max_results))
        except Exception as e:
            self.logger.error(f"Error during DuckDuckGo search: {e}")
            return f"Error during web search: {e}"

        if not search_results:
            self.logger.info(f"No results found for query: {query}")
            return "No results found."

        aggregated_text = ""
        for result in search_results:
            url = result.get("href") or result.get("url")
            if url:
                url, content = self.fetch_url(url)
                if content.startswith("Error:") or content.startswith("HTTP Error:"):
                    aggregated_text += f"\n\n--- Error from {url}: {content} ---\n"
                else:
                    aggregated_text += f"\n\n--- Content from {url} ---\n{content}\n"

        self.logger.info(f"Web search for query '{query}' completed successfully.")
        return aggregated_text.strip()

class WebSearchTool(ToolInterface):
    @property
    def name(self) -> str:
        return "WebSearchTool"

    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering WebSearchTool.")

        # Instantiate our local WebSearch implementation.
        web_search_instance = WebSearch()

        def websearch(query: str) -> str:
            context.info(f"Performing web search for: {query}")
            return web_search_instance.search(query)

        return [websearch]

def register():
    try:
        return WebSearchTool()
    except Exception as e:
        from core.utils.logger import get_logger
        get_logger().error(f"Error during websearch_tool registration: {e}")
        return None
