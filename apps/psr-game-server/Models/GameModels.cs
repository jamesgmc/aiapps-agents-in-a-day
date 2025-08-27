using System.ComponentModel.DataAnnotations;

namespace PsrGameServer.Models;

public enum Move
{
    None = 0,
    Rock = 1,
    Paper = 2,
    Scissors = 3
}

public enum MatchStatus
{
    Pending = 0,
    InProgress = 1,
    Completed = 2
}

public enum TournamentStatus
{
    WaitingForPlayers = 0,
    InProgress = 1,
    Completed = 2
}

public enum RoundStatus
{
    Waiting = 0,
    InProgress = 1,
    ResultsAvailable = 2,
    Completed = 3
}

public class Player
{
    public int Id { get; set; }
    
    [Required]
    [StringLength(50)]
    public string Name { get; set; } = string.Empty;
    
    public int TournamentId { get; set; }
    public Tournament Tournament { get; set; } = null!;
    
    public DateTime RegisteredAt { get; set; } = DateTime.UtcNow;
    
    public bool IsActive { get; set; } = true;
}

public class Tournament
{
    public int Id { get; set; }
    
    [StringLength(100)]
    public string Name { get; set; } = string.Empty;
    
    public TournamentStatus Status { get; set; } = TournamentStatus.WaitingForPlayers;
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    
    public DateTime? StartedAt { get; set; }
    
    public DateTime? CompletedAt { get; set; }
    
    public int? WinnerId { get; set; }
    public Player? Winner { get; set; }
    
    public List<Player> Players { get; set; } = new();
    
    public List<Match> Matches { get; set; } = new();
    
    public int CurrentRound { get; set; } = 1;
    
    public RoundStatus CurrentRoundStatus { get; set; } = RoundStatus.Waiting;
    
    public bool IsAcceptingPlayers => Status == TournamentStatus.WaitingForPlayers && Players.Count < 8;
}

public class Match
{
    public int Id { get; set; }
    
    public int TournamentId { get; set; }
    public Tournament Tournament { get; set; } = null!;
    
    public int Round { get; set; }
    
    public int? Player1Id { get; set; }
    public Player? Player1 { get; set; }
    
    public int? Player2Id { get; set; }
    public Player? Player2 { get; set; }
    
    public Move Player1Move { get; set; } = Move.None;
    
    public DateTime? Player1MoveSubmittedAt { get; set; }
    
    public Move Player2Move { get; set; } = Move.None;
    
    public DateTime? Player2MoveSubmittedAt { get; set; }
    
    public int? WinnerId { get; set; }
    public Player? Winner { get; set; }
    
    public MatchStatus Status { get; set; } = MatchStatus.Pending;
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    
    public DateTime? CompletedAt { get; set; }
    
    public bool BothPlayersSubmitted => Player1Move != Move.None && Player2Move != Move.None;
}

public class PlayerRegistrationRequest
{
    [Required]
    [StringLength(50, MinimumLength = 2)]
    public string Name { get; set; } = string.Empty;
}

public class BulkPlayerRegistrationRequest
{
    [Range(1, 8)]
    public int Count { get; set; } = 1;
    
    public bool UseAutoNames { get; set; } = true;
    
    public List<string> Names { get; set; } = new();
}

public class RoundControlRequest
{
    public int TournamentId { get; set; }
}

public class PlayerMoveRequest
{
    [Required]
    public Move Move { get; set; }
}

public class TournamentStateResponse
{
    public int TournamentId { get; set; }
    public string TournamentName { get; set; } = string.Empty;
    public TournamentStatus Status { get; set; }
    public int CurrentRound { get; set; }
    public RoundStatus CurrentRoundStatus { get; set; }
    public List<PlayerDto> Players { get; set; } = new();
    public List<MatchDto> Matches { get; set; } = new();
    public PlayerDto? Winner { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? StartedAt { get; set; }
    public DateTime? CompletedAt { get; set; }
}

public class PlayerDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public bool IsActive { get; set; }
    public DateTime RegisteredAt { get; set; }
}

public class MatchDto
{
    public int Id { get; set; }
    public int Round { get; set; }
    public PlayerDto? Player1 { get; set; }
    public PlayerDto? Player2 { get; set; }
    public Move Player1Move { get; set; }
    public DateTime? Player1MoveSubmittedAt { get; set; }
    public Move Player2Move { get; set; }
    public DateTime? Player2MoveSubmittedAt { get; set; }
    public PlayerDto? Winner { get; set; }
    public MatchStatus Status { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? CompletedAt { get; set; }
}

public class PlayerRegistrationResponse
{
    public int PlayerId { get; set; }
    public string PlayerName { get; set; } = string.Empty;
    public int TournamentId { get; set; }
    public string Message { get; set; } = string.Empty;
}

public class MoveSubmissionResponse
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
    public MatchDto? CurrentMatch { get; set; }
}

public class BulkPlayerRegistrationResponse
{
    public List<PlayerRegistrationResponse> Players { get; set; } = new();
    public int TournamentId { get; set; }
    public string Message { get; set; } = string.Empty;
}

public class RoundControlResponse
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
    public RoundStatus NewRoundStatus { get; set; }
    public int CurrentRound { get; set; }
}