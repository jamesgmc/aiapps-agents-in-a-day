

# Log in to Azure
az login

# AI Apps and Agents
az login --tenant f1146386-451a-4cc6-846b-a67f747921e9

# Set the subscription context
az account set --subscription 22f484c3-b754-45aa-8cec-e40bb48bcb34

# Create a new resource group
az group create --name rg-lab --location eastus2

#  What-If using the Bicep template and parameters file
az deployment group create --resource-group rg-lab --template-file ./foundry-deploy.bicep --what-if

# Deploy resources using the Bicep template and parameters file
az deployment group create --resource-group rg-lab --template-file ./foundry-deploy.bicep 


