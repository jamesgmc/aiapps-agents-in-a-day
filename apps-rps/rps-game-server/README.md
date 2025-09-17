# Paper-Scissors-Rock Tournament Game Server

A complete ASP.NET Core 8 web application for managing Paper-Scissors-Rock tournaments with questions and scoring.

## Features

### Tournament Management
- **Player Registration**: Register players via REST API
- **Tournament Control**: Start/stop tournaments via web interface
- **Round Management**: Create rounds with custom questions and answers
- **5-Round Format**: Complete tournament with 5 rounds
- **Real-time Updates**: Auto-refresh dashboard during active tournaments

### Scoring System
- **Correct Answer**: +10 points
- **RPS Win**: +20 points (Rock beats Scissors, Paper beats Rock, Scissors beats Paper)
- **RPS Tie**: +10 points (same move as server)
- **RPS Loss**: +0 points
- **Maximum per round**: 30 points (correct answer + RPS win)

### Web Interface
- **Dashboard**: Tournament status, player list, round management
- **Results**: Detailed round-by-round results and final standings
- **Grid View**: Comprehensive grid showing all player results across rounds
- **Responsive Design**: Bootstrap-based UI that works on all devices

### REST API
- `POST /api/player/register` - Register a new player
- `GET /api/player/{id}/status` - Get player's tournament status and current question
- `POST /api/player/submit-answer` - Submit answer and RPS move for current round
- `GET /api/player/{id}/results` - Get all results for a specific player
- `GET /api/tournament/status` - Get complete tournament state
- `GET /api/tournament/leaderboard` - Get current leaderboard (hidden during final 2 rounds)
- `GET /api/tournament/round/{id}/results` - Get detailed results for a specific round

## Running the Application

### Prerequisites
- .NET 8.0 SDK
- Any modern web browser

### Steps
1. Navigate to the project directory:
   ```bash
   cd apps-rps/rps-game-server
   ```

2. Run the application:
   ```bash
   dotnet run
   ```

3. Open your browser and navigate to:
   - **Web Interface**: http://localhost:5000
   - **API Documentation**: Available via the web interface

## Game Flow

### For Referees (Web Interface)
1. **Registration Phase**: Players register via API calls
2. **Start Tournament**: Click "Start Tournament" button
3. **Round Management**: 
   - Enter question and correct answer
   - Click "Start Round X" to begin the round
   - Monitor player submissions (shows X/Y submitted)
   - Click "End Round X" when all players have submitted or time is up
4. **Repeat**: Continue for all 5 rounds
5. **Final Results**: Click "End Tournament" to see final standings

### For Players (API)
1. **Register**: `POST /api/player/register` with player name
2. **Monitor Status**: `GET /api/player/{id}/status` to check tournament state
3. **Get Question**: When round is active, question is included in status response
4. **Submit Answer**: `POST /api/player/submit-answer` with answer and RPS move
5. **View Results**: `GET /api/player/{id}/results` to see personal results

## Tournament Rules

### Question Phase
- Each round includes a question that players must answer correctly
- Questions are set by the referee before starting each round
- Correct answers earn 30 points

### RPS Phase
- Players submit their RPS move (Rock=0, Paper=1, Scissors=2) along with their answer
- Server generates a random move for each round
- RPS results determine additional points:
  - Win: +20 points
  - Tie: +10 points
  - Loss: +0 points

### Leaderboard
- Shown during rounds 1-3
- Hidden during rounds 4-5 to maintain suspense
- Final standings revealed after tournament completion

### Final Results
- Top 3 winners displayed with medals (🥇🥈🥉)
- Complete leaderboard with all player scores
- Detailed round-by-round breakdown
- Grid view showing all player moves and results

## Architecture

- **ASP.NET Core 8**: Web framework with MVC + Web API
- **In-Memory Storage**: Thread-safe tournament state management
- **Bootstrap 5**: Responsive UI framework
- **SignalR-Ready**: Architecture supports real-time updates (can be added later)
- **CORS Enabled**: API accessible from external clients

## Testing

The application has been thoroughly tested with:
- ✅ Player registration and tournament flow
- ✅ Round creation and management
- ✅ Answer submission and scoring
- ✅ Leaderboard calculation
- ✅ All UI views and navigation
- ✅ Complete API functionality
- ✅ Multi-round tournament completion

## Future Enhancements

Potential improvements for production use:
- **Persistent Storage**: Database integration for tournament history
- **Real-time Updates**: SignalR for live dashboard updates
- **Authentication**: Player authentication and session management
- **Admin Panel**: Advanced tournament configuration
- **Statistics**: Historical tournament analytics
- **Mobile App**: Native mobile client for players