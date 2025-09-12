import json
import sys
from typing import Dict, Any


class SimpleWeatherServer:
    def __init__(self):
        self.weather_data = self._initialize_weather_data()
    
    def _initialize_weather_data(self) -> Dict[str, Any]:
        """Initialize mock weather data"""
        return {
            "sydney": {
                "location": "Sydney, Australia",
                "temperature": 22,
                "condition": "Partly Cloudy", 
                "humidity": 65,
                "wind_speed": 15,
                "wind_direction": "NE"
            },
            "melbourne": {
                "location": "Melbourne, Australia",
                "temperature": 18,
                "condition": "Overcast",
                "humidity": 70,
                "wind_speed": 12,
                "wind_direction": "SW"
            },
            "new york": {
                "location": "New York, USA",
                "temperature": 25,
                "condition": "Sunny",
                "humidity": 55,
                "wind_speed": 8,
                "wind_direction": "W"
            },
            "london": {
                "location": "London, UK",
                "temperature": 16,
                "condition": "Light Rain",
                "humidity": 80,
                "wind_speed": 10,
                "wind_direction": "SW"
            }
        }
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather for a location"""
        location_key = location.lower().strip()
        
        for key, data in self.weather_data.items():
            if key in location_key or location_key in key:
                return data
        
        return {
            "location": location,
            "temperature": 20,
            "condition": "Unknown",
            "humidity": 50,
            "wind_speed": 10,
            "wind_direction": "N",
            "note": "Mock data - location not found in database"
        }
    
    def get_weather_forecast(self, location: str, days: int = 3) -> Dict[str, Any]:
        """Get weather forecast for a location"""
        base_weather = self.get_weather(location)
        forecast = {
            "location": base_weather["location"],
            "forecast": []
        }
        
        conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Clear"]
        
        for day in range(min(days, 5)):
            day_weather = {
                "day": f"Day {day + 1}",
                "temperature_high": base_weather["temperature"] + (day % 3) - 1,
                "temperature_low": base_weather["temperature"] - 5 + (day % 2),
                "condition": conditions[day % len(conditions)],
                "chance_of_rain": min(20 + (day * 15), 80)
            }
            forecast["forecast"].append(day_weather)
        
        return forecast
    
    def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming requests"""
        method = request_data.get("method", "")
        params = request_data.get("params", {})
        request_id = request_data.get("id", 1)
        
        try:
            if method == "get_weather":
                location = params.get("location", "")
                result = self.get_weather(location)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            elif method == "get_weather_forecast":
                location = params.get("location", "")
                days = params.get("days", 3)
                result = self.get_weather_forecast(location, days)
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": result
                }
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
    
    def run(self):
        """Run the server in stdio mode"""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    server = SimpleWeatherServer()
    server.run()
