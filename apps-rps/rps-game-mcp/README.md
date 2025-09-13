# RPS Game MCP Server with Weather API

This directory contains an MCP (Model Context Protocol) server implementation using FastMCP that provides weather information with mock data.

## Features

- **MCP Protocol Support**: Implements MCP protocol with Server-Sent Events (SSE) transport
- **Weather API**: Provides mock weather data for any city
- **Hello Function**: Simple greeting function for testing
- **Mock Data**: Generates random weather conditions including temperature, weather condition, humidity, and wind speed

## Files

- `mcp-server.py`: The FastMCP server implementation with weather API
- `mcp-client.py`: Test client that connects to the MCP server and demonstrates functionality
- `requirements.txt`: Python dependencies

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

Run the MCP server:

```bash
python mcp-server.py
```

The server will start on `http://127.0.0.1:3111/mcp`

### Testing with the Client

In a separate terminal, run the test client:

```bash
python mcp-client.py
```

This will:
1. Connect to the MCP server using the MCP protocol
2. Initialize a session with Server-Sent Events
3. Demonstrate the weather API functionality
4. Show mock weather data for multiple cities

## API Functions

### `hello(name: str) -> str`
Returns a greeting message.

**Example:**
```
Input: "World"
Output: "Hello, World!"
```

### `get_weather(city: str) -> str`
Returns mock weather information for the specified city.

**Example:**
```
Input: "Sydney"
Output: "Weather in Sydney: 22°C, sunny, humidity 65%, wind 12 km/h"
```

The weather data includes:
- Temperature: Random value between -10°C and 39°C
- Condition: One of sunny, cloudy, rainy, snowy, foggy, windy
- Humidity: Random percentage between 20% and 100%
- Wind Speed: Random value between 0 and 30 km/h

## MCP Protocol Details

The server implements the MCP (Model Context Protocol) which allows AI agents and tools to communicate effectively. The implementation:

- Uses JSON-RPC 2.0 over HTTP with Server-Sent Events
- Supports proper MCP initialization handshake
- Handles session management with unique session IDs
- Provides tool discovery and execution capabilities

## Server Configuration

- **Host**: 127.0.0.1
- **Port**: 3111
- **Transport**: HTTP with SSE
- **Protocol Version**: 2024-11-05

## Development Notes

The server uses FastMCP for easy MCP protocol implementation. Each function decorated with `@mcp.tool` becomes available as an MCP tool that can be called by MCP clients.

The client demonstrates proper MCP protocol usage including:
- Session initialization
- Protocol version negotiation
- Capability advertisement
- Tool execution

## Testing

The included test client validates:
- MCP protocol initialization
- Server connectivity and response handling
- Weather API functionality with multiple cities
- Mock data generation and variation