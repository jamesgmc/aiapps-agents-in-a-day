import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, Optional


class SimpleWeatherMCPClient:
    def __init__(self, server_script_path: str = None):
        self.server_script_path = server_script_path or "rps_weather_mcp/simple_server.py"
        self.server_process = None
    
    async def start_server(self):
        """Start the weather server process"""
        if self.server_process:
            return
            
        self.server_process = await asyncio.create_subprocess_exec(
            sys.executable, self.server_script_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    
    async def stop_server(self):
        """Stop the weather server process"""
        if self.server_process:
            self.server_process.terminate()
            await self.server_process.wait()
            self.server_process = None
    
    async def call_method(self, method: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call a method on the weather server"""
        if not self.server_process:
            await self.start_server()
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        request_json = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_json.encode())
        await self.server_process.stdin.drain()
        
        try:
            response_line = await asyncio.wait_for(
                self.server_process.stdout.readline(), 
                timeout=5.0
            )
            if response_line:
                response = json.loads(response_line.decode().strip())
                return response
        except asyncio.TimeoutError:
            print("Timeout waiting for server response")
        except Exception as e:
            print(f"Error calling method: {e}")
        
        return None
    
    async def get_weather(self, location: str) -> str:
        """Get weather for a location"""
        response = await self.call_method("get_weather", {"location": location})
        if response and "result" in response:
            return json.dumps(response["result"], indent=2)
        return f"Error getting weather for {location}"
    
    async def get_weather_forecast(self, location: str, days: int = 3) -> str:
        """Get weather forecast for a location"""
        response = await self.call_method("get_weather_forecast", {
            "location": location,
            "days": days
        })
        if response and "result" in response:
            return json.dumps(response["result"], indent=2)
        return f"Error getting forecast for {location}"
    
    async def __aenter__(self):
        await self.start_server()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop_server()


class WeatherClient:
    """Synchronous wrapper for SimpleWeatherMCPClient"""
    
    def __init__(self, server_script_path: str = None):
        self.server_script_path = server_script_path
    
    def get_weather(self, location: str) -> str:
        """Get weather for a location synchronously"""
        async def _get_weather():
            async with SimpleWeatherMCPClient(self.server_script_path) as client:
                return await client.get_weather(location)
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _get_weather())
                    return future.result()
            else:
                return loop.run_until_complete(_get_weather())
        except RuntimeError:
            return asyncio.run(_get_weather())
    
    def get_weather_forecast(self, location: str, days: int = 3) -> str:
        """Get weather forecast for a location synchronously"""
        async def _get_forecast():
            async with SimpleWeatherMCPClient(self.server_script_path) as client:
                return await client.get_weather_forecast(location, days)
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, _get_forecast())
                    return future.result()
            else:
                return loop.run_until_complete(_get_forecast())
        except RuntimeError:
            return asyncio.run(_get_forecast())
