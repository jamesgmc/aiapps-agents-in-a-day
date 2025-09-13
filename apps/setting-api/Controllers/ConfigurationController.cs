using Microsoft.AspNetCore.Mvc;
using ConfigApi.Services;
using ConfigApi.Models;

namespace ConfigApi.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ConfigurationController : ControllerBase
{
    private readonly IConfigurationService _configurationService;
    private readonly ILogger<ConfigurationController> _logger;

    public ConfigurationController(IConfigurationService configurationService, ILogger<ConfigurationController> logger)
    {
        _configurationService = configurationService;
        _logger = logger;
    }

    /// <summary>
    /// Get a specific configuration item by key
    /// </summary>
    /// <param name="key">The configuration key to retrieve</param>
    /// <returns>Configuration item with value from Key Vault or configuration file</returns>
    [HttpGet]
    public async Task<IActionResult> GetConfiguration([FromQuery] string key)
    {
        if (string.IsNullOrWhiteSpace(key))
        {
            return BadRequest(new { error = "Key parameter is required" });
        }

        _logger.LogInformation("Retrieving configuration for key: {Key}", key);

        var config = await _configurationService.GetConfigurationAsync(key);
        
        if (config == null)
        {
            return NotFound(new { error = $"Configuration key '{key}' not found" });
        }

        return Ok(config);
    }

    /// <summary>
    /// Get all available configuration items
    /// </summary>
    /// <returns>List of all configuration items</returns>
    [HttpGet("all")]
    public async Task<IActionResult> GetAllConfigurations()
    {
        _logger.LogInformation("Retrieving all configuration items");

        var configs = await _configurationService.GetAllConfigurationsAsync();
        
        return Ok(new { 
            count = configs.Count,
            configurations = configs 
        });
    }

    /// <summary>
    /// Health check endpoint
    /// </summary>
    /// <returns>API status</returns>
    [HttpGet("health")]
    public IActionResult Health()
    {
        return Ok(new { 
            status = "healthy", 
            timestamp = DateTime.UtcNow,
            version = "1.0.0"
        });
    }
}
