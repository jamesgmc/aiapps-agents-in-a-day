using ConfigApi.Models;
using System.Text.Json;

namespace ConfigApi.Services;

public interface IConfigurationService
{
    Task<ConfigurationResponse?> GetConfigurationAsync(string key);
    Task<List<ConfigurationResponse>> GetAllConfigurationsAsync();
    Task<List<Setting>> GetAllSettingsAsync();
    Task<Setting?> GetSettingAsync(string id);
}

public class ConfigurationService : IConfigurationService
{
    private readonly List<Setting> _settings;
    private readonly ILogger<ConfigurationService> _logger;

    public ConfigurationService(IConfiguration configuration, ILogger<ConfigurationService> logger)
    {
        _logger = logger;
        
        // Load settings from JSON file
        var settingsFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "settings.json");
        _settings = LoadSettings(settingsFilePath);
    }

    public async Task<ConfigurationResponse?> GetConfigurationAsync(string key)
    {
        var setting = _settings.FirstOrDefault(s => 
            string.Equals(s.Id.ToString(), key, StringComparison.OrdinalIgnoreCase) ||
            string.Equals(s.Name, key, StringComparison.OrdinalIgnoreCase));

        if (setting == null)
        {
            _logger.LogWarning("Configuration key '{Key}' not found", key);
            return null;
        }

        await Task.CompletedTask;
        return new ConfigurationResponse
        {
            Id = setting.Id,
            Key = setting.Name,
            Description = setting.Description,
            Value = setting.Value,
        };
    }

    public async Task<List<ConfigurationResponse>> GetAllConfigurationsAsync()
    {
        await Task.CompletedTask;
        return _settings.Select(setting => new ConfigurationResponse
        {
            Id = setting.Id,
            Key = setting.Name,
            Description = setting.Description,
            Value = setting.Value,
        }).ToList();
    }

    public async Task<List<Setting>> GetAllSettingsAsync()
    {
        await Task.CompletedTask;
        return _settings.ToList();
    }

    public async Task<Setting?> GetSettingAsync(string id)
    {
        await Task.CompletedTask;
        return _settings.FirstOrDefault(s => string.Equals(s.Id.ToString(), id, StringComparison.OrdinalIgnoreCase));
    }

    private List<Setting> LoadSettings(string filePath)
    {
        try
        {
            if (!File.Exists(filePath))
            {
                _logger.LogError("Settings file not found at: {FilePath}", filePath);
                return new List<Setting>();
            }

            var jsonContent = File.ReadAllText(filePath);
            
            // First try to parse as array directly
            List<Setting>? settings;
            settings = JsonSerializer.Deserialize<List<Setting>>(jsonContent, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            _logger.LogInformation("Loaded {Count} settings from {FilePath}", 
                settings?.Count ?? 0, filePath);

            return settings ?? new List<Setting>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to load settings from {FilePath}", filePath);
            return new List<Setting>();
        }
    }
}