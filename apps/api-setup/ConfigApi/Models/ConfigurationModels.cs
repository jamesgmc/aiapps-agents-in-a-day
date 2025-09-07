namespace ConfigApi.Models;

public class ConfigurationItem
{
    public string Key { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? KeyVaultSecretName { get; set; }
    public string? Value { get; set; }
    public bool IsKeyVaultSecret { get; set; }
}

public class ConfigurationRoot
{
    public List<ConfigurationItem> Configurations { get; set; } = new();
}

public class ConfigurationResponse
{
    public string Key { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string? Value { get; set; }
    public bool IsFromKeyVault { get; set; }
    public string Source { get; set; } = string.Empty;
}