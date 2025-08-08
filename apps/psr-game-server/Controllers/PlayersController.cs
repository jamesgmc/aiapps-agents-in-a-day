using Microsoft.AspNetCore.Mvc;
using PsrGameServer.Models;
using PsrGameServer.Services;

namespace PsrGameServer.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PlayersController : ControllerBase
{
    private readonly IGameService _gameService;
    private readonly ILogger<PlayersController> _logger;

    public PlayersController(IGameService gameService, ILogger<PlayersController> logger)
    {
        _gameService = gameService;
        _logger = logger;
    }

    /// <summary>
    /// Register a new player for the tournament
    /// </summary>
    /// <param name="request">Player registration details</param>
    /// <returns>Registration result with player ID and tournament information</returns>
    [HttpPost("register")]
    public async Task<ActionResult<PlayerRegistrationResponse>> RegisterPlayer([FromBody] PlayerRegistrationRequest request)
    {
        try
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var result = await _gameService.RegisterPlayerAsync(request);
            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error registering player {Name}", request.Name);
            return StatusCode(500, new { error = "Internal server error occurred while registering player." });
        }
    }

    /// <summary>
    /// Submit a move for a player in their current match
    /// </summary>
    /// <param name="playerId">The player's ID</param>
    /// <param name="request">The move to submit</param>
    /// <returns>Move submission result</returns>
    [HttpPost("{playerId}/move")]
    public async Task<ActionResult<MoveSubmissionResponse>> SubmitMove(int playerId, [FromBody] PlayerMoveRequest request)
    {
        try
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var result = await _gameService.SubmitMoveAsync(playerId, request);
            
            if (!result.Success)
            {
                return BadRequest(result);
            }

            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error submitting move for player {PlayerId}", playerId);
            return StatusCode(500, new { error = "Internal server error occurred while submitting move." });
        }
    }

    /// <summary>
    /// Get the current match for a specific player
    /// </summary>
    /// <param name="playerId">The player's ID</param>
    /// <returns>Current match information</returns>
    [HttpGet("{playerId}/current-match")]
    public async Task<ActionResult<MatchDto>> GetCurrentMatch(int playerId)
    {
        try
        {
            var match = await _gameService.GetCurrentMatchForPlayerAsync(playerId);
            
            if (match == null)
            {
                return NotFound(new { message = "No active match found for player." });
            }

            var matchDto = new MatchDto
            {
                Id = match.Id,
                Round = match.Round,
                Player1 = match.Player1 != null ? new PlayerDto
                {
                    Id = match.Player1.Id,
                    Name = match.Player1.Name,
                    IsActive = match.Player1.IsActive,
                    RegisteredAt = match.Player1.RegisteredAt
                } : null,
                Player2 = match.Player2 != null ? new PlayerDto
                {
                    Id = match.Player2.Id,
                    Name = match.Player2.Name,
                    IsActive = match.Player2.IsActive,
                    RegisteredAt = match.Player2.RegisteredAt
                } : null,
                Player1Move = match.Player1Move,
                Player2Move = match.Player2Move,
                Winner = match.Winner != null ? new PlayerDto
                {
                    Id = match.Winner.Id,
                    Name = match.Winner.Name,
                    IsActive = match.Winner.IsActive,
                    RegisteredAt = match.Winner.RegisteredAt
                } : null,
                Status = match.Status,
                CreatedAt = match.CreatedAt,
                CompletedAt = match.CompletedAt
            };

            return Ok(matchDto);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error getting current match for player {PlayerId}", playerId);
            return StatusCode(500, new { error = "Internal server error occurred while getting current match." });
        }
    }
}
