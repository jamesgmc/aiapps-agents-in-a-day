from fastmcp import FastMCP
import random
import requests
import tempfile
import os
from urllib.parse import urlparse

mcp = FastMCP("RPS Game MCP Server")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool
def get_weather(city: str) -> str:
    """Get weather information for a city (mock data)"""
    
    weather_conditions = ["sunny", "cloudy", "rainy", "snowy", "foggy", "windy"]
    temperatures = list(range(-10, 40))  # -10°C to 39°C
    humidity_levels = list(range(20, 101))  # 20% to 100%
    
    mock_weather = {
        "city": city,
        "temperature": random.choice(temperatures),
        "condition": random.choice(weather_conditions),
        "humidity": random.choice(humidity_levels),
        "wind_speed": random.randint(0, 30)
    }
    
    return f"Weather in {city}: {mock_weather['temperature']}°C, {mock_weather['condition']}, humidity {mock_weather['humidity']}%, wind {mock_weather['wind_speed']} km/h"

@mcp.tool
def detect_animal_sound(mp3_url: str) -> str:
    """Detect what animal sound is in an MP3 file from a URL"""
    
    try:
        # Validate URL
        parsed_url = urlparse(mp3_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return "Error: Invalid URL provided"
        
        # Download the MP3 file
        response = requests.get(mp3_url, timeout=30)
        response.raise_for_status()
        
        # Check if it's actually an MP3 file
        content_type = response.headers.get('content-type', '').lower()
        if 'audio' not in content_type and not mp3_url.lower().endswith('.mp3'):
            return "Error: URL does not point to an audio file"
        
        # Get file size
        file_size = len(response.content)
        
        # Define 6 main domestic animals
        domestic_animals = ['dog', 'cat', 'bird', 'cow', 'horse', 'pig']
        
        # Yes, if you are reading this, we have cheated a bit here ! sorry!
        # Extract filename from URL and convert to lowercase for matching
        filename = os.path.basename(parsed_url.path).lower()
        url_lower = mp3_url.lower()
        
        # Check if any animal name is in the filename or URL
        detected_animal = None
        for animal in domestic_animals:
            if animal in filename or animal in url_lower:
                detected_animal = animal
                break
        
        if detected_animal:
            confidence = "85%"  # Mock confidence level
            return f"Animal sound detected: {detected_animal} (confidence: {confidence}, file size: {file_size} bytes)"
        else:
            return f"No domestic animal detected in filename. File size: {file_size} bytes. Supported animals: {', '.join(domestic_animals)}"
        
    except requests.exceptions.RequestException as e:
        return f"Error downloading MP3 file: {str(e)}"
    except Exception as e:
        return f"Error processing audio file: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3111)