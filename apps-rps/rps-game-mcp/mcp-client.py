import requests
import json

class MCPClient:
    def __init__(self, base_url: str = "http://127.0.0.1:3111/mcp"):
        self.base_url = base_url
    
    def call_tool(self, tool_name: str, arguments: dict):
        url = f"{self.base_url}/tools/call"
        payload = {
            "name": tool_name,
            "arguments": arguments
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def hello(self, name: str):
        return self.call_tool("hello", {"name": name})

def test_connection():
    client = MCPClient()
    
    print("Testing MCP server connection...")
    
    result = client.hello("World")
    print(f"Response: {result}")

if __name__ == "__main__":
    test_connection()
