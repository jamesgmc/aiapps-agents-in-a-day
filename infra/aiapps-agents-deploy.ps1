

# Log in to Azure
az login
az login --tenant a2ebc691-c318-4ec2-998a-a87c528378e0

# Set the subscription context
az account set --subscription 9df3a442-42f1-40dd-8547-958c3e01597a

# Create a new resource group
az group create --name rg-aiapps-agents --location eastus

#  What-If using the Bicep template and parameters file
az deployment group create --resource-group rg-aiapps-agents --template-file ./azuredeploy.bicep --parameters ./azuredeploy.parameters.json --what-if

# Deploy resources using the Bicep template and parameters file
az deployment group create --resource-group rg-aiapps-agents --template-file ./azuredeploy.bicep --parameters ./azuredeploy.parameters.json
