using Microsoft.EntityFrameworkCore;
using PsrGameServer.Data;
using PsrGameServer.Models;

namespace PsrGameServer.Services;

public interface IGameService
{
    Task<PlayerRegistrationResponse> RegisterPlayerAsync(PlayerRegistrationRequest request);
    Task<BulkPlayerRegistrationResponse> RegisterPlayersAsync(BulkPlayerRegistrationRequest request);
    Task<MoveSubmissionResponse> SubmitMoveAsync(int playerId, PlayerMoveRequest request);
    Task<TournamentStateResponse?> GetTournamentStateAsync(int? tournamentId = null);
    Task<Match?> GetCurrentMatchForPlayerAsync(int playerId);
    Task<RoundControlResponse> StartRoundAsync(int tournamentId);
    Task<RoundControlResponse> ReleaseResultsAsync(int tournamentId);
    string GenerateAutoPlayerName();
}

public class GameService : IGameService
{
    private readonly GameDbContext _context;
    private readonly ILogger<GameService> _logger;

    public GameService(GameDbContext context, ILogger<GameService> logger)
    {
        _context = context;
        _logger = logger;
    }

    public async Task<PlayerRegistrationResponse> RegisterPlayerAsync(PlayerRegistrationRequest request)
    {
        try
        {
            // Find or create an active tournament that's accepting players
            var activeTournament = await _context.Tournaments
                .Include(t => t.Players)
                .FirstOrDefaultAsync(t => t.Status == TournamentStatus.WaitingForPlayers && t.Players.Count < 8);

            if (activeTournament == null)
            {
                // Create a new tournament
                activeTournament = new Tournament
                {
                    Name = $"Tournament {DateTime.UtcNow:yyyy-MM-dd HH:mm}",
                    Status = TournamentStatus.WaitingForPlayers,
                    CreatedAt = DateTime.UtcNow,
                    CurrentRound = 1
                };
                _context.Tournaments.Add(activeTournament);
                await _context.SaveChangesAsync();
            }

            // Create the player
            var player = new Player
            {
                Name = request.Name.Trim(),
                TournamentId = activeTournament.Id,
                RegisteredAt = DateTime.UtcNow,
                IsActive = true
            };

            _context.Players.Add(player);
            await _context.SaveChangesAsync();

            // Check if we have 8 players to start the tournament
            var playerCount = await _context.Players.CountAsync(p => p.TournamentId == activeTournament.Id && p.IsActive);
            if (playerCount == 8)
            {
                await StartTournamentAsync(activeTournament.Id);
            }

            return new PlayerRegistrationResponse
            {
                PlayerId = player.Id,
                PlayerName = player.Name,
                TournamentId = activeTournament.Id,
                Message = playerCount == 8 ? "Tournament started! First round is ready." : $"Registered successfully. Waiting for {8 - playerCount} more players."
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error registering player: {Name}", request.Name);
            throw;
        }
    }

    public async Task<MoveSubmissionResponse> SubmitMoveAsync(int playerId, PlayerMoveRequest request)
    {
        try
        {
            var player = await _context.Players
                .Include(p => p.Tournament)
                .FirstOrDefaultAsync(p => p.Id == playerId && p.IsActive);

            if (player == null)
            {
                return new MoveSubmissionResponse
                {
                    Success = false,
                    Message = "Player not found or inactive."
                };
            }

            var currentMatch = await GetCurrentMatchForPlayerAsync(playerId);
            if (currentMatch == null)
            {
                return new MoveSubmissionResponse
                {
                    Success = false,
                    Message = "No active match found for player."
                };
            }

            // Update the player's move
            if (currentMatch.Player1Id == playerId)
            {
                if (currentMatch.Player1Move != Move.None)
                {
                    return new MoveSubmissionResponse
                    {
                        Success = false,
                        Message = "Move already submitted for this match."
                    };
                }
                currentMatch.Player1Move = request.Move;
            }
            else if (currentMatch.Player2Id == playerId)
            {
                if (currentMatch.Player2Move != Move.None)
                {
                    return new MoveSubmissionResponse
                    {
                        Success = false,
                        Message = "Move already submitted for this match."
                    };
                }
                currentMatch.Player2Move = request.Move;
            }
            else
            {
                return new MoveSubmissionResponse
                {
                    Success = false,
                    Message = "Player is not part of this match."
                };
            }

            currentMatch.Status = MatchStatus.InProgress;
            await _context.SaveChangesAsync();

            // Check if both players have submitted moves
            if (currentMatch.BothPlayersSubmitted)
            {
                await ProcessMatchResultAsync(currentMatch.Id);
            }

            var updatedMatch = await _context.Matches
                .Include(m => m.Player1)
                .Include(m => m.Player2)
                .Include(m => m.Winner)
                .FirstOrDefaultAsync(m => m.Id == currentMatch.Id);

            return new MoveSubmissionResponse
            {
                Success = true,
                Message = currentMatch.BothPlayersSubmitted ? "Match completed!" : "Move submitted. Waiting for opponent.",
                CurrentMatch = MapToMatchDto(updatedMatch!)
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error submitting move for player {PlayerId}", playerId);
            throw;
        }
    }

    public async Task<TournamentStateResponse?> GetTournamentStateAsync(int? tournamentId = null)
    {
        try
        {
            Tournament? tournament;

            if (tournamentId.HasValue)
            {
                tournament = await _context.Tournaments
                    .Include(t => t.Players)
                    .Include(t => t.Matches)
                        .ThenInclude(m => m.Player1)
                    .Include(t => t.Matches)
                        .ThenInclude(m => m.Player2)
                    .Include(t => t.Matches)
                        .ThenInclude(m => m.Winner)
                    .Include(t => t.Winner)
                    .FirstOrDefaultAsync(t => t.Id == tournamentId.Value);
            }
            else
            {
                // Get the most recent tournament
                tournament = await _context.Tournaments
                    .Include(t => t.Players)
                    .Include(t => t.Matches)
                        .ThenInclude(m => m.Player1)
                    .Include(t => t.Matches)
                        .ThenInclude(m => m.Player2)
                    .Include(t => t.Matches)
                        .ThenInclude(m => m.Winner)
                    .Include(t => t.Winner)
                    .OrderByDescending(t => t.CreatedAt)
                    .FirstOrDefaultAsync();
            }

            if (tournament == null)
                return null;

            return new TournamentStateResponse
            {
                TournamentId = tournament.Id,
                TournamentName = tournament.Name,
                Status = tournament.Status,
                CurrentRound = tournament.CurrentRound,
                CurrentRoundStatus = tournament.CurrentRoundStatus,
                Players = tournament.Players.Select(MapToPlayerDto).ToList(),
                Matches = tournament.Matches.OrderBy(m => m.Round).ThenBy(m => m.Id).Select(MapToMatchDto).ToList(),
                Winner = tournament.Winner != null ? MapToPlayerDto(tournament.Winner) : null,
                CreatedAt = tournament.CreatedAt,
                StartedAt = tournament.StartedAt,
                CompletedAt = tournament.CompletedAt
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting tournament state for tournament {TournamentId}", tournamentId);
            throw;
        }
    }

    public async Task<Match?> GetCurrentMatchForPlayerAsync(int playerId)
    {
        return await _context.Matches
            .Include(m => m.Player1)
            .Include(m => m.Player2)
            .Include(m => m.Winner)
            .Include(m => m.Tournament)
            .FirstOrDefaultAsync(m => 
                (m.Player1Id == playerId || m.Player2Id == playerId) && 
                m.Status != MatchStatus.Completed);
    }

    private async Task StartTournamentAsync(int tournamentId)
    {
        var tournament = await _context.Tournaments
            .Include(t => t.Players)
            .FirstOrDefaultAsync(t => t.Id == tournamentId);

        if (tournament == null || tournament.Players.Count != 8)
            return;

        tournament.Status = TournamentStatus.InProgress;
        tournament.StartedAt = DateTime.UtcNow;
        tournament.CurrentRoundStatus = RoundStatus.Waiting;

        // Create first round matches (4 matches for 8 players)
        var players = tournament.Players.OrderBy(p => p.RegisteredAt).ToList();
        for (int i = 0; i < players.Count; i += 2)
        {
            var match = new Match
            {
                TournamentId = tournamentId,
                Round = 1,
                Player1Id = players[i].Id,
                Player2Id = players[i + 1].Id,
                Status = MatchStatus.Pending,
                CreatedAt = DateTime.UtcNow
            };
            _context.Matches.Add(match);
        }

        await _context.SaveChangesAsync();
        _logger.LogInformation("Tournament {TournamentId} started with {PlayerCount} players", tournamentId, players.Count);
    }

    private async Task ProcessMatchResultAsync(int matchId)
    {
        var match = await _context.Matches
            .Include(m => m.Player1)
            .Include(m => m.Player2)
            .Include(m => m.Tournament)
            .FirstOrDefaultAsync(m => m.Id == matchId);

        if (match == null || !match.BothPlayersSubmitted)
            return;

        // Determine winner based on rock-paper-scissors rules
        var winner = DetermineWinner(match.Player1Move, match.Player2Move);
        
        if (winner == 1)
        {
            match.WinnerId = match.Player1Id;
        }
        else if (winner == 2)
        {
            match.WinnerId = match.Player2Id;
        }
        // If it's a tie, we could implement a tie-breaking mechanism or re-match

        match.Status = MatchStatus.Completed;
        match.CompletedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();

        // Check if round is complete and advance to next round
        await CheckAndAdvanceRoundAsync(match.Tournament);
    }

    private async Task CheckAndAdvanceRoundAsync(Tournament tournament)
    {
        var currentRoundMatches = await _context.Matches
            .Where(m => m.TournamentId == tournament.Id && m.Round == tournament.CurrentRound)
            .ToListAsync();

        // Only check if all matches are completed, but don't automatically advance
        // Round advancement should be controlled by the referee via ReleaseResultsAsync
        if (currentRoundMatches.All(m => m.Status == MatchStatus.Completed))
        {
            _logger.LogInformation("All matches completed for round {Round} in tournament {TournamentId}. Waiting for referee to release results.", 
                tournament.CurrentRound, tournament.Id);
        }
    }

    private async Task AdvanceToNextRoundAsync(Tournament tournament)
    {
        var currentRoundMatches = await _context.Matches
            .Where(m => m.TournamentId == tournament.Id && m.Round == tournament.CurrentRound)
            .ToListAsync();

        var winners = currentRoundMatches
            .Where(m => m.WinnerId.HasValue)
            .Select(m => m.WinnerId!.Value)
            .ToList();

        if (winners.Count == 1)
        {
            // Tournament is complete
            tournament.Status = TournamentStatus.Completed;
            tournament.WinnerId = winners.First();
            tournament.CompletedAt = DateTime.UtcNow;
            tournament.CurrentRoundStatus = RoundStatus.Completed;
            await _context.SaveChangesAsync();
            _logger.LogInformation("Tournament {TournamentId} completed. Winner: {WinnerId}", tournament.Id, winners.First());
        }
        else if (winners.Count > 1)
        {
            // Create next round matches
            tournament.CurrentRound++;
            tournament.CurrentRoundStatus = RoundStatus.Waiting;
            
            for (int i = 0; i < winners.Count; i += 2)
            {
                if (i + 1 < winners.Count)
                {
                    var nextMatch = new Match
                    {
                        TournamentId = tournament.Id,
                        Round = tournament.CurrentRound,
                        Player1Id = winners[i],
                        Player2Id = winners[i + 1],
                        Status = MatchStatus.Pending,
                        CreatedAt = DateTime.UtcNow
                    };
                    _context.Matches.Add(nextMatch);
                }
            }

            await _context.SaveChangesAsync();
            _logger.LogInformation("Tournament {TournamentId} advanced to round {Round}", tournament.Id, tournament.CurrentRound);
        }
    }

    private static int DetermineWinner(Move player1Move, Move player2Move)
    {
        if (player1Move == player2Move)
            return 0; // Tie

        return (player1Move, player2Move) switch
        {
            (Move.Rock, Move.Scissors) => 1,
            (Move.Paper, Move.Rock) => 1,
            (Move.Scissors, Move.Paper) => 1,
            _ => 2
        };
    }

    private static PlayerDto MapToPlayerDto(Player player)
    {
        return new PlayerDto
        {
            Id = player.Id,
            Name = player.Name,
            IsActive = player.IsActive,
            RegisteredAt = player.RegisteredAt
        };
    }

    private static MatchDto MapToMatchDto(Match match)
    {
        return new MatchDto
        {
            Id = match.Id,
            Round = match.Round,
            Player1 = match.Player1 != null ? MapToPlayerDto(match.Player1) : null,
            Player2 = match.Player2 != null ? MapToPlayerDto(match.Player2) : null,
            Player1Move = match.Player1Move,
            Player2Move = match.Player2Move,
            Winner = match.Winner != null ? MapToPlayerDto(match.Winner) : null,
            Status = match.Status,
            CreatedAt = match.CreatedAt,
            CompletedAt = match.CompletedAt
        };
    }

    public async Task<BulkPlayerRegistrationResponse> RegisterPlayersAsync(BulkPlayerRegistrationRequest request)
    {
        try
        {
            var response = new BulkPlayerRegistrationResponse();
            
            // Find or create an active tournament that's accepting players
            var activeTournament = await _context.Tournaments
                .Include(t => t.Players)
                .FirstOrDefaultAsync(t => t.Status == TournamentStatus.WaitingForPlayers && t.Players.Count < 8);

            if (activeTournament == null)
            {
                // Create a new tournament
                activeTournament = new Tournament
                {
                    Name = $"Tournament {DateTime.UtcNow:yyyy-MM-dd HH:mm}",
                    Status = TournamentStatus.WaitingForPlayers,
                    CreatedAt = DateTime.UtcNow,
                    CurrentRound = 1,
                    CurrentRoundStatus = RoundStatus.Waiting
                };
                _context.Tournaments.Add(activeTournament);
                await _context.SaveChangesAsync();
            }

            response.TournamentId = activeTournament.Id;
            
            var namesToRegister = new List<string>();
            if (request.UseAutoNames)
            {
                for (int i = 0; i < request.Count; i++)
                {
                    namesToRegister.Add(GenerateAutoPlayerName());
                }
            }
            else if (request.Names.Any())
            {
                namesToRegister.AddRange(request.Names.Take(request.Count));
            }
            else
            {
                throw new ArgumentException("Either UseAutoNames must be true or Names must be provided");
            }

            foreach (var name in namesToRegister)
            {
                // Check current player count from database
                var currentPlayerCount = await _context.Players.CountAsync(p => p.TournamentId == activeTournament.Id && p.IsActive);
                if (currentPlayerCount >= 8)
                    break;

                var player = new Player
                {
                    Name = name.Trim(),
                    TournamentId = activeTournament.Id,
                    RegisteredAt = DateTime.UtcNow,
                    IsActive = true
                };

                _context.Players.Add(player);
                await _context.SaveChangesAsync();

                response.Players.Add(new PlayerRegistrationResponse
                {
                    PlayerId = player.Id,
                    PlayerName = player.Name,
                    TournamentId = activeTournament.Id,
                    Message = "Registered successfully"
                });
            }

            // Check if we have 8 players to start the tournament
            var playerCount = await _context.Players.CountAsync(p => p.TournamentId == activeTournament.Id && p.IsActive);
            if (playerCount == 8)
            {
                await StartTournamentAsync(activeTournament.Id);
                response.Message = "Tournament started! All players registered.";
            }
            else
            {
                response.Message = $"Registered {response.Players.Count} players. Waiting for {8 - playerCount} more players.";
            }

            return response;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error registering bulk players");
            throw;
        }
    }

    public async Task<RoundControlResponse> StartRoundAsync(int tournamentId)
    {
        try
        {
            var tournament = await _context.Tournaments
                .Include(t => t.Matches)
                .FirstOrDefaultAsync(t => t.Id == tournamentId);

            if (tournament == null)
            {
                return new RoundControlResponse
                {
                    Success = false,
                    Message = "Tournament not found."
                };
            }

            if (tournament.Status != TournamentStatus.InProgress)
            {
                return new RoundControlResponse
                {
                    Success = false,
                    Message = "Tournament is not in progress."
                };
            }

            if (tournament.CurrentRoundStatus != RoundStatus.Waiting)
            {
                return new RoundControlResponse
                {
                    Success = false,
                    Message = $"Round {tournament.CurrentRound} is not waiting to start. Current status: {tournament.CurrentRoundStatus}"
                };
            }

            // Start the round
            tournament.CurrentRoundStatus = RoundStatus.InProgress;
            
            // Update all pending matches in current round to in-progress
            var currentRoundMatches = await _context.Matches
                .Where(m => m.TournamentId == tournamentId && m.Round == tournament.CurrentRound && m.Status == MatchStatus.Pending)
                .ToListAsync();

            foreach (var match in currentRoundMatches)
            {
                match.Status = MatchStatus.InProgress;
            }

            await _context.SaveChangesAsync();
            
            _logger.LogInformation("Round {Round} started for tournament {TournamentId}", tournament.CurrentRound, tournamentId);

            return new RoundControlResponse
            {
                Success = true,
                Message = $"Round {tournament.CurrentRound} started successfully!",
                NewRoundStatus = tournament.CurrentRoundStatus,
                CurrentRound = tournament.CurrentRound
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error starting round for tournament {TournamentId}", tournamentId);
            throw;
        }
    }

    public async Task<RoundControlResponse> ReleaseResultsAsync(int tournamentId)
    {
        try
        {
            var tournament = await _context.Tournaments
                .Include(t => t.Matches)
                .FirstOrDefaultAsync(t => t.Id == tournamentId);

            if (tournament == null)
            {
                return new RoundControlResponse
                {
                    Success = false,
                    Message = "Tournament not found."
                };
            }

            if (tournament.CurrentRoundStatus != RoundStatus.InProgress)
            {
                return new RoundControlResponse
                {
                    Success = false,
                    Message = $"Round {tournament.CurrentRound} is not in progress. Current status: {tournament.CurrentRoundStatus}"
                };
            }

            // Check if all matches in current round are completed
            var currentRoundMatches = await _context.Matches
                .Where(m => m.TournamentId == tournamentId && m.Round == tournament.CurrentRound)
                .ToListAsync();

            if (!currentRoundMatches.All(m => m.Status == MatchStatus.Completed))
            {
                return new RoundControlResponse
                {
                    Success = false,
                    Message = "Not all matches in current round are completed."
                };
            }

            // Release results
            tournament.CurrentRoundStatus = RoundStatus.ResultsAvailable;
            await _context.SaveChangesAsync();

            _logger.LogInformation("Results released for round {Round} in tournament {TournamentId}", tournament.CurrentRound, tournamentId);

            // After releasing results, advance to next round
            await AdvanceToNextRoundAsync(tournament);

            return new RoundControlResponse
            {
                Success = true,
                Message = $"Results for round {tournament.CurrentRound} have been released!",
                NewRoundStatus = tournament.CurrentRoundStatus,
                CurrentRound = tournament.CurrentRound
            };
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error releasing results for tournament {TournamentId}", tournamentId);
            throw;
        }
    }

    public string GenerateAutoPlayerName()
    {
        var adjectives = new[] { "Swift", "Mighty", "Clever", "Bold", "Quick", "Strong", "Smart", "Brave", "Sharp", "Fast" };
        var nouns = new[] { "Warrior", "Fighter", "Champion", "Player", "Ninja", "Master", "Hero", "Legend", "Ace", "Pro" };
        
        var random = new Random();
        var adjective = adjectives[random.Next(adjectives.Length)];
        var noun = nouns[random.Next(nouns.Length)];
        var number = random.Next(100, 999);
        
        return $"{adjective}{noun}{number}";
    }
}