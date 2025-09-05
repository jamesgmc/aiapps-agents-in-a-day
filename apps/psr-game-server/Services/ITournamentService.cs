using PsrGameServer.Models;

namespace PsrGameServer.Services;

public interface ITournamentService
{
    // Player registration
    RegisterPlayerResponse RegisterPlayer(string playerName);
    
    // Tournament management
    Tournament GetTournament();
    bool StartTournament();
    bool EndTournament();
    
    // Round management
    bool StartRound(int roundNumber, string question, string correctAnswer);
    bool EndRound(int roundNumber);
    Round? GetCurrentRound();
    
    // Player actions
    TournamentStatusResponse GetTournamentStatus(int playerId);
    SubmitAnswerResponse SubmitAnswer(SubmitAnswerRequest request);
    
    // Results and leaderboard
    List<LeaderboardEntry> GetLeaderboard(bool hideForLastTwoRounds = false);
    List<RoundResultEntry> GetRoundResults(int roundNumber);
    List<PlayerRoundResult> GetPlayerResults(int playerId);
}