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
    /// Get tournament results (alias for state with completed status)
    /// </summary>
    /// <param name="tournamentId">Optional tournament ID. If not provided, returns the most recent tournament.</param>
    /// <returns>Tournament results</returns>
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