# PSR Game Client

A Node.js web application that acts as a player client for the Paper-Scissors-Rock tournament game server.

## Features

- **Player Registration**: Enter player name and register with the game server
- **Tournament Status Monitoring**: Real-time polling of tournament and round status
- **Automatic Question Answering**: Attempts to answer questions automatically
- **Random Move Selection**: Randomly chooses Rock, Paper, or Scissors moves
- **Results Display**: Shows round results and final tournament standings

## Game Flow

1. **Registration**: Player enters their name and registers with the server
2. **Tournament Wait**: Client waits for referee to start the tournament
3. **Round Participation**: For each of 5 rounds:
   - Wait for round to start
   - Receive question from server
   - Attempt to answer the question
   - Select random RPS move (Rock, Paper, Scissors)
   - Submit answer and move to server
   - Display round results
4. **Final Results**: Display final tournament results

## API Communication

The client communicates with the PSR game server via these REST endpoints:

- `POST /api/player/register` - Register player with name
- `GET /api/player/{id}/status` - Get tournament and round status
- `POST /api/player/submit-answer` - Submit answer and RPS move
- `GET /api/player/{id}/results` - Get player results

## Running the Client

### Prerequisites

- Node.js 16+ 
- PSR Game Server running on http://localhost:5000

### Steps

1. Navigate to the client directory:
   ```bash
   cd apps/psr-game-client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the client:
   ```bash
   npm start
   ```

4. Open your browser and navigate to: http://localhost:3000

## Configuration

- **Server URL**: Configured to connect to `http://localhost:5000` by default
- **Client Port**: Runs on port 3000 by default
- **Polling Interval**: Checks server status every 2 seconds during active gameplay

## Architecture

- **Express.js**: Web server for the client interface
- **Axios**: HTTP client for API communication with game server
- **Real-time Polling**: Continuously monitors game state
- **Simple UI**: Clean web interface for player interaction

## Testing

To test the complete game flow:

1. Start the PSR game server (`cd apps/psr-game-server && dotnet run`)
2. Start this client (`cd apps/psr-game-client && npm start`)
3. Open the client in browser (http://localhost:3000)
4. Enter player name and register
5. Use the server web interface (http://localhost:5000) to start tournament and rounds
6. Watch the client automatically participate in the game

## Future Enhancements

- Multiple client support for testing
- Better question answering with AI integration
- Enhanced UI with real-time updates
- Strategic RPS move selection
- Tournament history and statistics