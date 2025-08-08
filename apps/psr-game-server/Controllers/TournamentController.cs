using Microsoft.AspNetCore.Mvc;
using PsrGameServer.Models;
using PsrGameServer.Services;

namespace PsrGameServer.Controllers;

[ApiController]
[Route("api/[controller]")]
public class TournamentController : ControllerBase
{
    private readonly IGameService _gameService;
    private readonly ILogger<TournamentController> _logger;

    public TournamentController(IGameService gameService, ILogger<TournamentController> logger)
    {
        _gameService = gameService;
        _logger = logger;
    }

    /// <summary>
    /// Get the current tournament state
    /// </summary>
    /// <param name="tournamentId">Optional tournament ID. If not provided, returns the most recent tournament.</param>
    /// <returns>Tournament state information</returns>
    [HttpGet("state")]
    public async Task<ActionResult<TournamentStateResponse>> GetTournamentState([FromQuery] int? tournamentId = null)
    {
        try
        {
            var result = await _gameService.GetTournamentStateAsync(tournamentId);
            
            if (result == null)
            {
                return NotFound(new { message = "No tournament found." });
            }

            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting tournament state for tournament {TournamentId}", tournamentId);
            return StatusCode(500, new { error = "Internal server error occurred while getting tournament state." });
        }
    }

    /// <summary>
    /// Start a round (referee control)
    /// </summary>
    /// <param name="request">Round control request with tournament ID</param>
    /// <returns>Round control result</returns>
    [HttpPost("start-round")]
    public async Task<ActionResult<RoundControlResponse>> StartRound([FromBody] RoundControlRequest request)
    {
        try
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var result = await _gameService.StartRoundAsync(request.TournamentId);
            
            if (!result.Success)
            {
                return BadRequest(result);
            }

            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error starting round for tournament {TournamentId}", request.TournamentId);
            return StatusCode(500, new { error = "Internal server error occurred while starting round." });
        }
    }

    /// <summary>
    /// Release round results (referee control)
    /// </summary>
    /// <param name="request">Round control request with tournament ID</param>
    /// <returns>Round control result</returns>
    [HttpPost("release-results")]
    public async Task<ActionResult<RoundControlResponse>> ReleaseResults([FromBody] RoundControlRequest request)
    {
        try
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var result = await _gameService.ReleaseResultsAsync(request.TournamentId);
            
            if (!result.Success)
            {
                return BadRequest(result);
            }

            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error releasing results for tournament {TournamentId}", request.TournamentId);
            return StatusCode(500, new { error = "Internal server error occurred while releasing results." });
        }
    }
    [HttpGet("results")]
    public async Task<ActionResult<TournamentStateResponse>> GetTournamentResults([FromQuery] int? tournamentId = null)
    {
        try
        {
            var result = await _gameService.GetTournamentStateAsync(tournamentId);
            
            if (result == null)
            {
                return NotFound(new { message = "No tournament found." });
            }

            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting tournament results for tournament {TournamentId}", tournamentId);
            return StatusCode(500, new { error = "Internal server error occurred while getting tournament results." });
        }
    }
}