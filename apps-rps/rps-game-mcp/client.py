import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List


class WeatherMCPClient:
    def __init__(self, server_path: str = None):
        self.server_path = server_path or "python -m rps_weather_mcp.server"
        self.server_process = None
    
    async def start_server(self):
        """Start the MCP server process"""
        self.server_process = await asyncio.create_subprocess_shell(
            self.server_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    
    async def stop_server(self):
        """Stop the MCP server process"""
        if self.server_process:
            self.server_process.terminate()
            await self.server_process.wait()
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the MCP server"""
        if not self.server_process:
            await self.start_server()
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        request_json = json.dumps(request) + "\n"
        self.server_process.stdin.write(request_json.encode())
        await self.server_process.stdin.drain()
        
        response_line = await self.server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.decode().strip())
            if "result" in response:
                return response["result"][0]["text"]
        
        return "Error: No response from MCP server"
    
    async def get_weather(self, location: str) -> str:
        """Get weather for a location"""
        return await self.call_tool("get_weather", {"location": location})
    
    async def get_weather_forecast(self, location: str, days: int = 3) -> str:
        """Get weather forecast for a location"""
        return await self.call_tool("get_weather_forecast", {
            "location": location,
            "days": days
        })
    
    async def __aenter__(self):
        await self.start_server()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop_server()


class WeatherMCPClientSync:
    """Synchronous wrapper for WeatherMCPClient"""
    
    def __init__(self, server_path: str = None):
        self.server_path = server_path
        self.client = None
    
    def start(self):
        """Start the MCP client"""
        self.client = WeatherMCPClient(self.server_path)
    
    def get_weather(self, location: str) -> str:
        """Get weather for a location synchronously"""
        if not self.client:
            self.start()
        
        async def _get_weather():
            async with self.client as client:
                return await client.get_weather(location)
        
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(_get_weather())
        except RuntimeError:
            return asyncio.run(_get_weather())
    
    def get_weather_forecast(self, location: str, days: int = 3) -> str:
        """Get weather forecast for a location synchronously"""
        if not self.client:
            self.start()
        
        async def _get_forecast():
            async with self.client as client:
                return await client.get_weather_forecast(location, days)
        
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(_get_forecast())
        except RuntimeError:
            return asyncio.run(_get_forecast())
