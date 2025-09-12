#!/usr/bin/env python3

import asyncio
import subprocess
import sys
import os

def show_mcp_server_info():
    print("=== MCP Weather Server Information ===")
    print()
    
    # Server details
    print("🌦️  Server Name: rps-weather-mcp")
    print("📦  Server Version: 0.1.0")
    print("🔧  Protocol: Model Context Protocol (MCP)")
    print("📡  Transport: stdio (Standard Input/Output)")
    print()
    
    # Connection details
    print("🔌 Connection Details:")
    print("   • This MCP server runs via stdio (not HTTP)")
    print("   • No traditional URL - communicates via stdin/stdout")
    print("   • Connect using MCP-compatible clients")
    print()
    
    # Available tools
    print("🛠️  Available Tools:")
    print("   1. get_weather")
    print("      - Get current weather for a location")
    print("      - Parameters: location (string)")
    print()
    print("   2. get_weather_forecast")
    print("      - Get weather forecast for a location")
    print("      - Parameters: location (string), days (1-5)")
    print()
    
    # File paths
    current_dir = os.getcwd()
    print("📁 Server Files:")
    print(f"   • Main Server: {current_dir}\\server.py")
    print(f"   • Simple Server: {current_dir}\\simple_server.py")
    print(f"   • Client: {current_dir}\\client.py")
    print(f"   • Simple Client: {current_dir}\\simple_client.py")
    print()
    
    # Usage examples
    print("🚀 Usage Examples:")
    print("   • Run server: python server.py")
    print("   • Test with simple client: python simple_client.py")
    print("   • Test weather call: python test_weather_mcp.py")
    print()
    
    # MCP Integration
    print("🔗 MCP Client Integration:")
    print("   • Use with Claude Desktop MCP configuration")
    print("   • Integrate with VS Code MCP extensions")
    print("   • Connect via any MCP-compatible client")
    print()
    
    print("✅ Server is ready to accept MCP connections via stdio")

if __name__ == "__main__":
    show_mcp_server_info()
