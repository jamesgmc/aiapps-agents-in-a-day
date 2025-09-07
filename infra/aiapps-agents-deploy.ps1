
$ResourceGroupName = "rg-aiapps-agents"
$Location = "Australia East"
$bicepPath = "aiapps-agents-deploy.bicep"
$parametersPath = "aiapps-agents-deploy.parameters.json"

# Create resource group if it doesn't exist
$rgExists = az group exists --name $ResourceGroupName
if ($rgExists -eq "false") {
    az group create --name $ResourceGroupName --location $Location
}

# Validate Bicep template
Write-Host "Validating Bicep template..." -ForegroundColor Yellow
$validationResult = az deployment group validate `
    --resource-group $ResourceGroupName `
    --template-file $bicepPath `
    --parameters $parametersPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "Template validation failed!" -ForegroundColor Red
    exit 1
}
Write-Host "Template validation successful!" -ForegroundColor Green

# Deploy Bicep template
$deploymentName = "main-deployment-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Write-Host "Starting deployment: $deploymentName" -ForegroundColor Yellow
az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file $bicepPath `
    --parameters $parametersPath `
    --name $deploymentName
