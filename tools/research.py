import requests
from typing import List, Callable
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from tqdm import tqdm
import pdfplumber
from io import BytesIO
import time
from core.utils.logger import get_logger
from core.tools.tool_interface import ToolInterface, ToolContext
from concurrent.futures import ThreadPoolExecutor, as_completed

class Research:
    def __init__(self):
        self.logger = get_logger()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
        }
        self.timeout = 45  # seconds

    def search(self, query: str) -> str:
        try:
            search_results = DDGS().text(query, max_results=7)
        except Exception as e:
            self.logger.error("DuckDuckGo search failed for query '%s': %s", query, e)
            return f"Search error: {e}"
        
        if not search_results:
            self.logger.success("No results for query '%s'.", query)
            return "No results found."

        aggregated_text = ""
        for result in search_results:
            url = result.get("href") or result.get("url")
            if not url or not url.startswith(("http://", "https://")):
                self.logger.warning("Invalid or missing URL in result for query '%s': %s", query, url)
                continue
            
            aggregated_text += f"\n\n--- Content from: {url} ---\n"
            content = self.fetch_url(url)
            aggregated_text += content
            
        return aggregated_text.strip()

    def fetch_url(self, url: str) -> str:
        retries = 3
        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url, headers=self.headers, timeout=self.timeout)
                
                if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "").lower()
                    if "application/pdf" in content_type:
                        with pdfplumber.open(BytesIO(response.content)) as pdf:
                            text = ""
                            for page in pdf.pages:
                                text += page.extract_text() or ""
                        return text[:10000]  # Limit to 10,000 characters
                    elif "text/html" in content_type:
                        soup = BeautifulSoup(response.text, "html.parser")
                        for element in soup(["script", "style", "nav", "footer"]):
                            element.decompose()
                        page_text = soup.get_text(separator=" ", strip=True)
                        return page_text[:10000]
                    else:
                        return f"Unsupported content type: {content_type}"
                elif response.status_code == 403:
                    return f"HTTP 403 Forbidden: Access denied for {url}"
                elif response.status_code == 404:
                    return f"HTTP 404 Not Found: {url}"
                elif response.status_code == 429:
                    self.logger.warning("Rate limit hit on %s (attempt %d)", url, attempt)
                    if attempt < retries:
                        time.sleep(2 ** attempt + 5)  # Exponential backoff
                    else:
                        return f"Rate limit exceeded for {url} after {retries} attempts"
                else:
                    return f"HTTP {response.status_code} error for {url}"
                    
            except requests.Timeout:
                self.logger.error("Timeout fetching %s on attempt %d", url, attempt)
                if attempt < retries:
                    time.sleep(2 ** attempt)
                else:
                    return f"Timeout fetching {url} after {retries} attempts"
            except Exception as e:
                self.logger.error("Error fetching %s on attempt %d: %s", url, attempt, e)
                if attempt < retries:
                    time.sleep(2 ** attempt)
                else:
                    return f"Error fetching {url} after {retries} attempts: {e}"

    def research(self, queries: List[str]) -> str:
        self.logger.success("Initiating research for %d queries.", len(queries))
        aggregated_results = []
        with ThreadPoolExecutor(max_workers=len(queries)) as executor:
            future_to_query = {executor.submit(self.search, query): query for query in queries}
            for future in tqdm(as_completed(future_to_query), total=len(queries), desc="Processing queries"):
                query = future_to_query[future]
                try:
                    result = future.result()
                except Exception as exc:
                    self.logger.error("Query %s generated an exception: %s", query, exc)
                    result = f"Error processing query: {exc}"
                aggregated_results.append(f"\n\n=== Results for '{query}' ===\n{result}")
        self.logger.success("Research completed successfully.")
        return f"Research Data:\n{''.join(aggregated_results)}"

class ResearchTool(ToolInterface):
    @property
    def name(self) -> str:
        return "ResearchTool"

    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering ResearchTool tools.")

        def search_research(query: List[str]) -> str:
            context.success(f"Executing research for queries: {query}")
            researcher = Research()
            research = researcher.research(queries=query)
            return f"Research results for {query}:\n{research}"
        
        return [search_research]

def register():
    try:
        return ResearchTool()
    except Exception as e:
        from core.utils.logger import get_logger
        get_logger().error(f"Error during ResearchTool registration: {e}")
        return None