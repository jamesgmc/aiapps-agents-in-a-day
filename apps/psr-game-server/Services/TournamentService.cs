using PsrGameServer.Models;
using System.Collections.Concurrent;

namespace PsrGameServer.Services;

public class TournamentService : ITournamentService
{
    private readonly Tournament _tournament = new();
    private readonly object _lock = new();
    private int _nextPlayerId = 1;

    public Tournament GetTournament()
    {
        lock (_lock)
        {
            return _tournament;
        }
    }

    public RegisterPlayerResponse RegisterPlayer(string playerName)
    {
        lock (_lock)
        {
            if (_tournament.Status != TournamentStatus.Pending)
            {
                return new RegisterPlayerResponse
                {
                    PlayerId = 0,
                    Message = "Tournament has already started or completed"
                };
            }

            var player = new Player
            {
                Id = _nextPlayerId++,
                Name = playerName,
                RegisteredAt = DateTime.UtcNow
            };

            _tournament.Players.Add(player);

            return new RegisterPlayerResponse
            {
                PlayerId = player.Id,
                Message = $"Player {playerName} registered successfully with ID {player.Id}"
            };
        }
    }

    public bool StartTournament()
    {
        lock (_lock)
        {
            if (_tournament.Status != TournamentStatus.Pending)
                return false;

            _tournament.Status = TournamentStatus.InProgress;
            _tournament.StartedAt = DateTime.UtcNow;
            _tournament.CurrentRound = 1;

            // Initialize rounds
            for (int i = 1; i <= Tournament.MaxRounds; i++)
            {
                _tournament.Rounds.Add(new Round { RoundNumber = i });
            }

            return true;
        }
    }

    public bool EndTournament()
    {
        lock (_lock)
        {
            if (_tournament.Status != TournamentStatus.InProgress)
                return false;

            _tournament.Status = TournamentStatus.Completed;
            _tournament.EndedAt = DateTime.UtcNow;
            return true;
        }
    }

    public bool StartRound(int roundNumber, string question, string correctAnswer)
    {
        lock (_lock)
        {
            if (_tournament.Status != TournamentStatus.InProgress)
                return false;

            var round = _tournament.Rounds.FirstOrDefault(r => r.RoundNumber == roundNumber);
            if (round == null || round.Status != RoundStatus.Pending)
                return false;

            round.Status = RoundStatus.InProgress;
            round.Question = question;
            round.CorrectAnswer = correctAnswer;
            round.ServerMove = GenerateRandomMove();
            round.StartedAt = DateTime.UtcNow;

            // Initialize player results for this round
            foreach (var player in _tournament.Players)
            {
                round.PlayerResults.Add(new PlayerRoundResult
                {
                    PlayerId = player.Id,
                    RoundNumber = roundNumber
                });
            }

            _tournament.CurrentRound = roundNumber;
            return true;
        }
    }

    public bool EndRound(int roundNumber)
    {
        lock (_lock)
        {
            var round = _tournament.Rounds.FirstOrDefault(r => r.RoundNumber == roundNumber);
            if (round == null || round.Status != RoundStatus.InProgress)
                return false;

            round.Status = RoundStatus.Completed;
            round.EndedAt = DateTime.UtcNow;

            // Calculate scores for this round
            CalculateRoundScores(round);

            return true;
        }
    }

    public Round? GetCurrentRound()
    {
        lock (_lock)
        {
            return _tournament.Rounds.FirstOrDefault(r => r.RoundNumber == _tournament.CurrentRound);
        }
    }

    public TournamentStatusResponse GetTournamentStatus(int playerId)
    {
        lock (_lock)
        {
            var currentRound = GetCurrentRound();
            return new TournamentStatusResponse
            {
                TournamentStatus = _tournament.Status,
                CurrentRound = _tournament.CurrentRound,
                CurrentRoundStatus = currentRound?.Status,
                CurrentQuestion = currentRound?.Status == RoundStatus.InProgress ? currentRound.Question : null,
                CanSubmit = currentRound?.Status == RoundStatus.InProgress && 
                          !currentRound.PlayerResults.Any(pr => pr.PlayerId == playerId && pr.HasSubmitted)
            };
        }
    }

    public SubmitAnswerResponse SubmitAnswer(SubmitAnswerRequest request)
    {
        lock (_lock)
        {
            var round = _tournament.Rounds.FirstOrDefault(r => r.RoundNumber == request.RoundNumber);
            if (round == null || round.Status != RoundStatus.InProgress)
            {
                return new SubmitAnswerResponse
                {
                    Success = false,
                    Message = "Round is not active"
                };
            }

            var playerResult = round.PlayerResults.FirstOrDefault(pr => pr.PlayerId == request.PlayerId);
            if (playerResult == null)
            {
                return new SubmitAnswerResponse
                {
                    Success = false,
                    Message = "Player not found in round"
                };
            }

            if (playerResult.HasSubmitted)
            {
                return new SubmitAnswerResponse
                {
                    Success = false,
                    Message = "Answer already submitted for this round"
                };
            }

            playerResult.Answer = request.Answer;
            playerResult.Move = request.Move;
            playerResult.SubmittedAt = DateTime.UtcNow;
            playerResult.AnswerCorrect = string.Equals(request.Answer.Trim(), round.CorrectAnswer.Trim(), StringComparison.OrdinalIgnoreCase);

            return new SubmitAnswerResponse
            {
                Success = true,
                Message = "Answer submitted successfully"
            };
        }
    }

    public List<LeaderboardEntry> GetLeaderboard(bool hideForLastTwoRounds = false)
    {
        lock (_lock)
        {
            if (hideForLastTwoRounds && _tournament.CurrentRound >= Tournament.MaxRounds - 1)
            {
                return new List<LeaderboardEntry>();
            }

            var leaderboard = _tournament.Players
                .Select(p => new LeaderboardEntry
                {
                    PlayerId = p.Id,
                    PlayerName = p.Name,
                    TotalScore = p.TotalScore
                })
                .OrderByDescending(le => le.TotalScore)
                .ThenBy(le => le.PlayerName)
                .ToList();

            for (int i = 0; i < leaderboard.Count; i++)
            {
                leaderboard[i].Position = i + 1;
            }

            return leaderboard;
        }
    }

    public List<RoundResultEntry> GetRoundResults(int roundNumber)
    {
        lock (_lock)
        {
            var round = _tournament.Rounds.FirstOrDefault(r => r.RoundNumber == roundNumber);
            if (round == null)
                return new List<RoundResultEntry>();

            return round.PlayerResults
                .Join(_tournament.Players, pr => pr.PlayerId, p => p.Id, (pr, p) => new RoundResultEntry
                {
                    PlayerId = p.Id,
                    PlayerName = p.Name,
                    Answer = pr.Answer,
                    Move = pr.Move,
                    AnswerCorrect = pr.AnswerCorrect,
                    ServerMove = round.ServerMove,
                    WonRound = pr.Move.HasValue && DetermineWinner(pr.Move.Value, round.ServerMove),
                    Score = pr.Score
                })
                .OrderByDescending(rre => rre.Score)
                .ThenBy(rre => rre.PlayerName)
                .ToList();
        }
    }

    public List<PlayerRoundResult> GetPlayerResults(int playerId)
    {
        lock (_lock)
        {
            return _tournament.Rounds
                .SelectMany(r => r.PlayerResults)
                .Where(pr => pr.PlayerId == playerId)
                .OrderBy(pr => pr.RoundNumber)
                .ToList();
        }
    }

    private Move GenerateRandomMove()
    {
        var random = new Random();
        var moves = Enum.GetValues<Move>();
        return moves[random.Next(moves.Length)];
    }

    private void CalculateRoundScores(Round round)
    {
        foreach (var result in round.PlayerResults)
        {
            if (!result.HasSubmitted || !result.Move.HasValue)
            {
                result.Score = 0;
                continue;
            }

            int score = 0;

            // Score for correct answer
            if (result.AnswerCorrect)
            {
                score += 10;
            }

            // Score for winning rock-paper-scissors
            if (DetermineWinner(result.Move.Value, round.ServerMove))
            {
                score += 20;
            }
            else if (result.Move.Value == round.ServerMove)
            {
                // Tie gives half points
                score += 10;
            }

            result.Score = score;

            // Update player total score
            var player = _tournament.Players.FirstOrDefault(p => p.Id == result.PlayerId);
            if (player != null)
            {
                player.TotalScore += score;
            }
        }
    }

    private bool DetermineWinner(Move playerMove, Move serverMove)
    {
        return playerMove switch
        {
            Move.Rock => serverMove == Move.Scissors,
            Move.Paper => serverMove == Move.Rock,
            Move.Scissors => serverMove == Move.Paper,
            _ => false
        };
    }
}