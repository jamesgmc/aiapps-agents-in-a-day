using Azure.Security.KeyVault.Secrets;
using Azure.Identity;
using ConfigApi.Models;
using System.Text.Json;

namespace ConfigApi.Services;

public interface IConfigurationService
{
    Task<ConfigurationResponse?> GetConfigurationAsync(string key);
    Task<List<ConfigurationResponse>> GetAllConfigurationsAsync();
}

public class ConfigurationService : IConfigurationService
{
    private readonly SecretClient? _secretClient;
    private readonly List<ConfigurationItem> _configurationItems;
    private readonly ILogger<ConfigurationService> _logger;

    public ConfigurationService(IConfiguration configuration, ILogger<ConfigurationService> logger)
    {
        _logger = logger;
        
        // Load configuration items from JSON file
        var configFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "config-items.json");
        _configurationItems = LoadConfigurationItems(configFilePath);

        // Initialize Key Vault client if URL is provided
        var keyVaultUrl = configuration["KeyVault:VaultUrl"];
        if (!string.IsNullOrEmpty(keyVaultUrl))
        {
            try
            {
                _secretClient = new SecretClient(new Uri(keyVaultUrl), new DefaultAzureCredential());
                _logger.LogInformation("Key Vault client initialized with URL: {KeyVaultUrl}", keyVaultUrl);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to initialize Key Vault client");
            }
        }
        else
        {
            _logger.LogWarning("Key Vault URL not configured. Key Vault secrets will not be available.");
        }
    }

    public async Task<ConfigurationResponse?> GetConfigurationAsync(string key)
    {
        var configItem = _configurationItems.FirstOrDefault(c => 
            string.Equals(c.Key, key, StringComparison.OrdinalIgnoreCase));

        if (configItem == null)
        {
            _logger.LogWarning("Configuration key '{Key}' not found", key);
            return null;
        }

        return await CreateConfigurationResponseAsync(configItem);
    }

    public async Task<List<ConfigurationResponse>> GetAllConfigurationsAsync()
    {
        var responses = new List<ConfigurationResponse>();

        foreach (var configItem in _configurationItems)
        {
            var response = await CreateConfigurationResponseAsync(configItem);
            responses.Add(response);
        }

        return responses;
    }

    private async Task<ConfigurationResponse> CreateConfigurationResponseAsync(ConfigurationItem configItem)
    {
        string? value = null;
        bool isFromKeyVault = false;
        string source = "Configuration File";

        if (configItem.IsKeyVaultSecret && _secretClient != null && !string.IsNullOrEmpty(configItem.KeyVaultSecretName))
        {
            try
            {
                var secretResponse = await _secretClient.GetSecretAsync(configItem.KeyVaultSecretName);
                value = secretResponse.Value.Value;
                isFromKeyVault = true;
                source = "Key Vault";
                _logger.LogInformation("Retrieved secret '{SecretName}' from Key Vault", configItem.KeyVaultSecretName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to retrieve secret '{SecretName}' from Key Vault", configItem.KeyVaultSecretName);
                value = "[Key Vault Error: " + ex.Message + "]";
                source = "Key Vault (Error)";
            }
        }
        else if (!configItem.IsKeyVaultSecret)
        {
            value = configItem.Value;
            source = "Configuration File";
        }
        else
        {
            value = "[Key Vault not configured]";
            source = "Configuration File (Key Vault unavailable)";
        }

        return new ConfigurationResponse
        {
            Key = configItem.Key,
            Description = configItem.Description,
            Value = value,
            IsFromKeyVault = isFromKeyVault,
            Source = source
        };
    }

    private List<ConfigurationItem> LoadConfigurationItems(string filePath)
    {
        try
        {
            if (!File.Exists(filePath))
            {
                _logger.LogError("Configuration file not found at: {FilePath}", filePath);
                return new List<ConfigurationItem>();
            }

            var jsonContent = File.ReadAllText(filePath);
            var configRoot = JsonSerializer.Deserialize<Models.ConfigurationRoot>(jsonContent, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            _logger.LogInformation("Loaded {Count} configuration items from {FilePath}", 
                configRoot?.Configurations?.Count ?? 0, filePath);

            return configRoot?.Configurations ?? new List<ConfigurationItem>();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to load configuration items from {FilePath}", filePath);
            return new List<ConfigurationItem>();
        }
    }
}