from fastmcp import FastMCP
import random

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

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3111)