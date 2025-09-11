using Microsoft.AspNetCore.Mvc;
using RpsGameServer.Models;
using RpsGameServer.Services;

namespace RpsGameServer.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TournamentController : ControllerBase
{
    private readonly ITournamentService _tournamentService;

    public TournamentController(ITournamentService tournamentService)
    {
        _tournamentService = tournamentService;
    }

    [HttpGet("status")]
    public ActionResult<Tournament> GetTournamentStatus()
    {
        var tournament = _tournamentService.GetTournament();
        return Ok(tournament);
    }

    [HttpGet("leaderboard")]
    public ActionResult<List<LeaderboardEntry>> GetLeaderboard()
    {
        var leaderboard = _tournamentService.GetLeaderboard(hideForLastTwoRounds: true);
        return Ok(leaderboard);
    }

    [HttpGet("round/{roundNumber}/results")]
    public ActionResult<List<RoundResultEntry>> GetRoundResults(int roundNumber)
    {
        var results = _tournamentService.GetRoundResults(roundNumber);
        return Ok(results);
    }
}