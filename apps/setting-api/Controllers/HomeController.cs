using Microsoft.AspNetCore.Mvc;
using ConfigApi.Services;

namespace ConfigApi.Controllers;

public class HomeController : Controller
{
    private readonly IConfigurationService _configurationService;
    private readonly ILogger<HomeController> _logger;

    public HomeController(IConfigurationService configurationService, ILogger<HomeController> logger)
    {
        _configurationService = configurationService;
        _logger = logger;
    }

    public async Task<IActionResult> Index()
    {
        _logger.LogInformation("Loading home page with settings list");
        
        var settings = await _configurationService.GetAllSettingsAsync();
        
        return View(settings);
    }
}
