#!/usr/bin/env python3

import requests
import json

def test_weather_server():
    base_url = "http://localhost:8000"
    
    print("=== Testing RPS Weather MCP Server (HTTP Mode) ===")
    print()
    
    # Test server info
    print("1. Testing server info...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            info = response.json()
            print(f"   ✅ Server: {info['name']} v{info['version']}")
            print(f"   📝 Description: {info['description']}")
        else:
            print(f"   ❌ Failed to get server info: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test health check
    print("2. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"   ✅ Status: {health['status']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test tools listing
    print("3. Testing tools listing...")
    try:
        response = requests.get(f"{base_url}/tools")
        if response.status_code == 200:
            tools = response.json()
            print(f"   ✅ Available tools: {len(tools['tools'])}")
            for tool in tools['tools']:
                print(f"      - {tool['name']}: {tool['description']}")
        else:
            print(f"   ❌ Tools listing failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test weather endpoint
    print("4. Testing weather endpoint...")
    locations = ["Sydney", "New York", "London", "Unknown City"]
    
    for location in locations:
        try:
            response = requests.post(
                f"{base_url}/weather",
                json={"location": location}
            )
            if response.status_code == 200:
                weather = response.json()
                if weather['success']:
                    data = weather['data']
                    print(f"   ✅ {data['location']}: {data['temperature']}°C, {data['condition']}")
                else:
                    print(f"   ❌ {location}: {weather['error']}")
            else:
                print(f"   ❌ Weather request failed for {location}: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error for {location}: {e}")
    
    print()
    
    # Test forecast endpoint
    print("5. Testing forecast endpoint...")
    try:
        response = requests.post(
            f"{base_url}/forecast",
            json={"location": "Sydney", "days": 3}
        )
        if response.status_code == 200:
            forecast = response.json()
            if forecast['success']:
                data = forecast['data']
                print(f"   ✅ {data['location']} - {data['forecast_days']} day forecast:")
                for day in data['forecast']:
                    print(f"      Day {day['day']}: {day['temperature_high']}°/{day['temperature_low']}°C, {day['condition']}")
            else:
                print(f"   ❌ Forecast failed: {forecast['error']}")
        else:
            print(f"   ❌ Forecast request failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("=== Test Complete ===")
    print()
    print("🌐 Server URLs:")
    print(f"   • Main: {base_url}")
    print(f"   • API Docs: {base_url}/docs")
    print(f"   • Health: {base_url}/health")
    print(f"   • Tools: {base_url}/tools")

if __name__ == "__main__":
    test_weather_server()
