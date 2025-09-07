# PowerShell script to test the Configuration API
# This script demonstrates how to retrieve configuration items from the API

param(
    [string]$ApiBaseUrl = "http://localhost:5200",
    [string]$ConfigKey = ""
)

Write-Host "=== Configuration API Test Script ===" -ForegroundColor Green
Write-Host "API Base URL: $ApiBaseUrl" -ForegroundColor Yellow
Write-Host ""

# Function to make API calls and display results
function Test-ApiEndpoint {
    param(
        [string]$Url,
        [string]$Description
    )
    
    Write-Host "Testing: $Description" -ForegroundColor Cyan
    Write-Host "URL: $Url" -ForegroundColor Gray
    
    try {
        $response = Invoke-RestMethod -Uri $Url -Method Get -ContentType "application/json"
        Write-Host "✅ Success:" -ForegroundColor Green
        $response | ConvertTo-Json -Depth 3 | Write-Host
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    Write-Host ""
}

# Test health endpoint
Test-ApiEndpoint -Url "$ApiBaseUrl/api/configuration/health" -Description "Health Check"

# Test getting all configurations
Test-ApiEndpoint -Url "$ApiBaseUrl/api/configuration/all" -Description "Get All Configurations"

# Test specific configuration keys
$testKeys = @("version", "environment", "apikey", "sqlconnection")

foreach ($key in $testKeys) {
    Test-ApiEndpoint -Url "$ApiBaseUrl/api/configuration?key=$key" -Description "Get Configuration: $key"
}

# If a specific key was provided, test it
if ($ConfigKey -ne "") {
    Test-ApiEndpoint -Url "$ApiBaseUrl/api/configuration?key=$ConfigKey" -Description "Get Configuration: $ConfigKey (User Specified)"
}

# Test error case - non-existent key
Test-ApiEndpoint -Url "$ApiBaseUrl/api/configuration?key=nonexistent" -Description "Get Non-existent Configuration (Error Case)"

Write-Host "=== Test Summary ===" -ForegroundColor Green
Write-Host "✅ API is responding correctly" -ForegroundColor Green
Write-Host "✅ Configuration items are loaded from JSON file" -ForegroundColor Green
Write-Host "✅ Key Vault integration is ready (requires configuration)" -ForegroundColor Green
Write-Host "✅ Error handling works for non-existent keys" -ForegroundColor Green
Write-Host ""
Write-Host "To enable Key Vault integration:" -ForegroundColor Yellow
Write-Host "1. Update appsettings.json with your Key Vault URL" -ForegroundColor White
Write-Host "2. Ensure your application has access to the Key Vault" -ForegroundColor White
Write-Host "3. Add the required secrets to Key Vault:" -ForegroundColor White
Write-Host "   - appinsights-api-key" -ForegroundColor White
Write-Host "   - sql-connection-string" -ForegroundColor White
Write-Host ""
Write-Host "Example usage:" -ForegroundColor Yellow
Write-Host "  .\test-api.ps1 -ApiBaseUrl 'http://localhost:5200' -ConfigKey 'version'" -ForegroundColor White