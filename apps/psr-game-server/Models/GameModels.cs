namespace PsrGameServer.Models;

public record QuestionAnswer(string Question, string Answer);

public enum TournamentStatus
{
    Pending,
    InProgress,
    Completed
}

public enum RoundStatus
{
    Pending,
    InProgress,
    Completed
}

public enum Move
{
    Rock,
    Paper,
    Scissors
}

public class Player
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public int TotalScore { get; set; }
    public DateTime RegisteredAt { get; set; }
}

public class PlayerRoundResult
{
    public int PlayerId { get; set; }
    public int RoundNumber { get; set; }
    public string? Answer { get; set; }
    public Move? Move { get; set; }
    public bool AnswerCorrect { get; set; }
    public int Score { get; set; }
    public DateTime? SubmittedAt { get; set; }
    public bool HasSubmitted => SubmittedAt.HasValue;
}

public class Round
{
    public int RoundNumber { get; set; }
    public RoundStatus Status { get; set; }
    public string Question { get; set; } = string.Empty;
    public string CorrectAnswer { get; set; } = string.Empty;
    public Move ServerMove { get; set; }
    public List<PlayerRoundResult> PlayerResults { get; set; } = new();
    public DateTime? StartedAt { get; set; }
    public DateTime? EndedAt { get; set; }
}

public class Tournament
{
    public TournamentStatus Status { get; set; }
    public List<Player> Players { get; set; } = new();
    public List<Round> Rounds { get; set; } = new();
    public int CurrentRound { get; set; } = 1;
    public DateTime? StartedAt { get; set; }
    public DateTime? EndedAt { get; set; }

    public const int MaxRounds = 5;
}

public class RegisterPlayerRequest
{
    public string Name { get; set; } = string.Empty;
}

public class RegisterPlayerResponse
{
    public int PlayerId { get; set; }
    public string Message { get; set; } = string.Empty;
}

public class SubmitAnswerRequest
{
    public int PlayerId { get; set; }
    public int RoundNumber { get; set; }
    public string Answer { get; set; } = string.Empty;
    public Move Move { get; set; }
}

public class SubmitAnswerResponse
{
    public bool Success { get; set; }
    public string Message { get; set; } = string.Empty;
}

public class TournamentStatusResponse
{
    public TournamentStatus TournamentStatus { get; set; }
    public int CurrentRound { get; set; }
    public RoundStatus? CurrentRoundStatus { get; set; }
    public string? CurrentQuestion { get; set; }
    public bool CanSubmit { get; set; }
}

public class LeaderboardEntry
{
    public int PlayerId { get; set; }
    public string PlayerName { get; set; } = string.Empty;
    public int TotalScore { get; set; }
    public int Position { get; set; }
}

public class RoundResultEntry
{
    public int PlayerId { get; set; }
    public string PlayerName { get; set; } = string.Empty;
    public string? Answer { get; set; }
    public Move? Move { get; set; }
    public bool AnswerCorrect { get; set; }
    public Move ServerMove { get; set; }
    public bool WonRound { get; set; }
    public int Score { get; set; }
}