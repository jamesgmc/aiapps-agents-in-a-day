
# Paper Scissors Rock Game Server

A complete tournament-style Paper Scissors Rock game server built with ASP.NET Core Web API and a responsive web frontend.

## Features

- **Tournament Management**: Automatic 8-player tournament creation and bracket progression
- **REST API**: Complete endpoints for player registration and move submission
- **Live Tournament Display**: Real-time tournament bracket with emoji move visualization
- **Rock-Paper-Scissors Logic**: Proper game rule implementation with winner determination
- **Responsive UI**: Bootstrap-based frontend with tournament bracket display
- **Real-time Updates**: SignalR integration for live tournament updates


## Game Flow

1. **Player Registration**: Players register via API and receive unique player IDs
2. **Tournament Creation**: When 8 players are registered, tournament automatically starts
3. **Match Play**: Players submit moves (Rock=1, Paper=2, Scissors=3) via API
4. **Winner Determination**: Server applies rock-paper-scissors rules to determine winners
5. **Tournament Progression**: Winners advance through elimination rounds
6. **Championship**: Final match determines tournament winner

## Technology Stack

- **Backend**: ASP.NET Core 8.0 Web API
- **Database**: Entity Framework Core (In-Memory)
- **Real-time**: SignalR for live updates
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **API Documentation**: Swagger/OpenAPI


## Game Rules

- **Rock (🪨)** beats **Scissors (✂️)**
- **Paper (📄)** beats **Rock (🪨)**
- **Scissors (✂️)** beats **Paper (📄)**

## Tournament Structure

- **Round 1**: 8 players → 4 matches → 4 winners
- **Round 2**: 4 players → 2 matches → 2 winners  
- **Round 3**: 2 players → 1 match → 1 champion

## Development

The project is structured as a standard ASP.NET Core Web API with:

- **Controllers**: API endpoints for players and tournament
- **Services**: Game logic and tournament management
- **Models**: Data models for players, matches, and tournaments
- **Data**: Entity Framework DbContext for data persistence
- **Hubs**: SignalR hub for real-time updates
- **wwwroot**: Static web files for the frontend

## API Documentation

When running in development mode, Swagger documentation is available at:
`http://localhost:5096/swagger`

