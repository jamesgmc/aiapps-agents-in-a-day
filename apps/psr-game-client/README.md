
# Paper Scissors Rock Game Client

A Python client for the PSR Game Server that allows players to participate in tournament-style Paper Scissors Rock games.

## Features

- **Player Registration**: Register with the tournament server and receive unique player ID
- **Tournament Participation**: Automatically handle tournament flow and round progression
- **Multiple Play Modes**: Interactive mode for human players, auto mode for bots
- **Real-time Polling**: Monitor tournament state and match status
- **Smart Round Detection**: Automatically detect when new rounds start
- **Tournament Status**: View current tournament state and player standings

## Installation

1. Navigate to the client directory:
```bash
cd apps/psr-game-client
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode
Play the tournament manually with user input:
```bash
python main.py play
```

### Automated Mode
Let the client play automatically with random moves:
```bash
python main.py auto "Bot Player Name"
```

### Tournament Status
Check the current tournament status:
```bash
python main.py status
```

### Custom Server
Connect to a different server:
```bash
python main.py --server http://localhost:5096 play
```

### Verbose Logging
Enable detailed logging:
```bash
python main.py --verbose play
```

## Game Flow

1. **Registration**: Client registers player with server and receives unique ID
2. **Wait for Tournament**: Polls server until tournament starts (8 players required)
3. **Round Play**: For each round:
   - Wait for round to start
   - Get current match information
   - Submit move (Rock, Paper, or Scissors)
   - Wait for match completion and see results
4. **Tournament Progression**: Winners advance to next round, losers are eliminated
5. **Tournament End**: Play continues until tournament completion

## API Integration

The client integrates with the PSR Game Server REST API:

- `POST /api/players/register` - Register new player
- `GET /api/tournament/state` - Get tournament state
- `GET /api/players/{id}/current-match` - Get current match
- `POST /api/players/{id}/move` - Submit move

## Configuration

Edit `config.py` to customize:
- Server URL and API endpoints
- Polling intervals and timeouts
- Move mappings and game settings

## Game Rules

- **Rock (🪨)** beats **Scissors (✂️)**
- **Paper (📄)** beats **Rock (🪨)**
- **Scissors (✂️)** beats **Paper (📄)**

## Tournament Structure

- **Registration**: Up to 8 players
- **Round 1**: 8 players → 4 matches → 4 winners
- **Round 2**: 4 players → 2 matches → 2 winners
- **Round 3**: 2 players → 1 match → 1 champion

## Examples

### Complete Tournament Flow
```bash
# Terminal 1 - Start server (if needed)
cd ../psr-game-server
dotnet run

# Terminal 2 - Player 1 (Interactive)
cd ../psr-game-client
python main.py play

# Terminal 3 - Player 2 (Auto)
python main.py auto "Bot1"

# Terminal 4 - More players as needed
python main.py auto "Bot2"
# ... continue until 8 players registered

# Terminal 5 - Monitor status
python main.py status
```

## Error Handling

The client includes comprehensive error handling for:
- Network connection issues
- Invalid server responses
- Tournament state changes
- Player elimination
- Timeout scenarios

## Development

The client is structured with:
- `psr_game_client.py` - Main client class with API integration
- `main.py` - CLI interface and user interaction
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies






