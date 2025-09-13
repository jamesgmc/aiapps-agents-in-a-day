# Variables
$displayName = "sp-az-lab-on-demand"

# Create the app registration
$app = az ad app create --display-name $displayName | ConvertFrom-Json

# Generate a client secret
$secret = az ad app credential reset --id $app.appId | ConvertFrom-Json

# Output the app registration details
Write-Output "App Registration Details:"
Write-Output "App ID: $($app.appId)"
Write-Output "Client Secret: $($secret.password)"

