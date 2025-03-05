import requests
from bs4 import BeautifulSoup
from core.utils.logger import get_logger
from core.tools.tool_interface import ToolInterface, ToolContext
from typing import List, Callable

logger = get_logger()

def get_temperature() -> str:
    """
    Fetches the current temperature based on the user's IP location.

    Returns:
        str: A message with the current temperature or an error message.
    """
    try:
        ip_address = requests.get('https://api.ipify.org').text
        url_geo = f'https://get.geojs.io/v1/ip/geo/{ip_address}.json'
        response_geo = requests.get(url_geo)
        geo_data = response_geo.json()
        city = geo_data.get('city', 'your city')
        
        search_query = f"temperature in {city}"
        url_search = f"https://www.google.com/search?q={search_query}"
        response_search = requests.get(url_search)
        soup = BeautifulSoup(response_search.text, "html.parser")
        temp_tag = soup.find("div", class_="BNeawe")
        if temp_tag:
            temperature = temp_tag.text
            logger.success(f"Temperature fetched for {city}: {temperature}")
            return f"Current temperature in {city} is {temperature}"
        else:
            return f"Unable to fetch temperature information for {city}."
    except Exception as e:
        logger.error(f"Error fetching temperature: {e}")
        return f"Error fetching temperature: {e}"

class WeatherTool(ToolInterface):
    @property
    def name(self) -> str:
        return "WeatherTool"

    def register(self, context: ToolContext) -> List[Callable]:
        context.success("Registering WeatherTool tools.")

        def get_weather(city: str) -> str:
            try:
                response = requests.get(f"https://wttr.in/{city}?format=3")
                if response.status_code == 200:
                    context.success(f"Weather for {city}: {response.text}")
                    return response.text
                else:
                    context.error("Failed to get weather information.")
                    return "Error retrieving weather information"
            except Exception as e:
                context.error(f"Error retrieving weather: {e}")
                return f"Error retrieving weather: {e}"

        return [get_weather]

def register():
    try:
        return WeatherTool()
    except Exception as e:
        logger.error(f"Error during weather_tool registration: {e}")
        return None 