# Azure Infrastructure for Agentic AI App

This directory contains the Infrastructure as Code (IaC) templates for deploying the Agentic AI App workshop environment to Azure.

## Architecture Overview

The infrastructure deploys the following Azure resources:

### Core AI & Analytics Services
- **Azure AI Foundry Workspace**: Hub for AI model development and deployment
- **Azure AI Search**: Intelligent search service for RAG implementations
- **Azure Cosmos DB**: NoSQL database for agent state and knowledge storage
- **Application Insights**: Application performance monitoring and analytics

### Compute & Hosting Services  
- **Azure Function App**: Serverless compute for event-driven agent functions
- **Azure Web App**: Hosting for the game server (.NET application)
- **Azure Static Web App**: Hosting for the client-side applications
- **Azure Logic App**: Workflow automation and orchestration

### Security & Storage Services
- **Azure Key Vault**: Secure secrets and configuration management
- **Azure Storage Account**: Blob storage for files and artifacts
- **Azure Container Registry**: Private container image registry
- **Log Analytics Workspace**: Centralized logging and monitoring

## File Structure

```
infra/
├── main.bicep                    # Main infrastructure template
├── parameters.dev.json           # Development environment parameters
├── parameters.staging.json       # Staging environment parameters
├── parameters.prod.json          # Production environment parameters
└── README.md                     # This documentation
```

## Prerequisites

Before deploying the infrastructure, ensure you have:

1. **Azure Subscription**: Active Azure subscription with appropriate permissions
2. **Azure CLI**: Installed and authenticated (`az login`)
3. **Bicep CLI**: Installed for template validation (`az bicep install`)
4. **GitHub Secrets**: Required secrets configured for GitHub Actions deployment

### Required GitHub Secrets

Configure the following secrets in your GitHub repository:

```bash
AZURE_CREDENTIALS          # Service principal credentials (JSON format)
AZURE_SUBSCRIPTION_ID       # Azure subscription ID
AZURE_TENANT_ID            # Azure tenant ID
AZURE_CLIENT_ID            # Service principal client ID
AZURE_CLIENT_SECRET        # Service principal client secret
```

#### Creating Azure Service Principal

```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "sp-agentic-ai-app-github" \
  --role contributor \
  --scopes /subscriptions/{subscription-id} \
  --sdk-auth

# The output should be saved as AZURE_CREDENTIALS secret
```

## Deployment Methods

### 1. GitHub Actions (Recommended)

The repository includes automated deployment workflows:

#### Manual Deployment
Navigate to **Actions** → **Deploy Azure Infrastructure** → **Run workflow**

Choose:
- Environment: `dev`, `staging`, or `prod`
- Location: Azure region (default: `East US`)

#### Automatic Deployment
- **Development**: Automatically deploys on push to `main` branch
- **Staging/Production**: Manual deployment only

### 2. Local Deployment

#### Validate Template
```bash
# Validate bicep syntax
az bicep build --file infra/main.bicep

# Validate deployment
az deployment group validate \
  --resource-group rg-agentic-ai-app-dev \
  --template-file infra/main.bicep \
  --parameters @infra/parameters.dev.json
```

#### Deploy Infrastructure
```bash
# Create resource group
az group create \
  --name rg-agentic-ai-app-dev \
  --location "East US"

# Deploy template
az deployment group create \
  --resource-group rg-agentic-ai-app-dev \
  --template-file infra/main.bicep \
  --parameters @infra/parameters.dev.json \
  --name infra-deployment-$(date +%Y%m%d-%H%M%S)
```

#### Preview Changes
```bash
# Run what-if analysis
az deployment group what-if \
  --resource-group rg-agentic-ai-app-dev \
  --template-file infra/main.bicep \
  --parameters @infra/parameters.dev.json
```

## Environment Configuration

### Development Environment
- **Resource Group**: `rg-agentic-ai-app-dev`
- **SKU Tiers**: Basic/Standard (cost-optimized)
- **Scaling**: Minimal instances
- **Location**: East US (default)

### Staging Environment
- **Resource Group**: `rg-agentic-ai-app-staging`
- **SKU Tiers**: Standard (production-like)
- **Scaling**: Moderate instances
- **Location**: East US (default)

### Production Environment
- **Resource Group**: `rg-agentic-ai-app-prod`
- **SKU Tiers**: Premium (high availability)
- **Scaling**: Auto-scaling enabled
- **Location**: East US (default)

## Customization

### Modifying Parameters

Edit the appropriate parameter file:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": {
      "value": "West US 2"        // Change deployment region
    },
    "environment": {
      "value": "dev"              // Environment suffix
    },
    "appName": {
      "value": "my-custom-app"    // Application name prefix
    }
  }
}
```

### Resource Naming Convention

Resources follow this naming pattern:
- Format: `{appName}-{environment}-{resourceType}-{uniqueSuffix}`
- Example: `agentic-ai-app-dev-func-abc123`

## Post-Deployment Configuration

After successful deployment:

1. **Configure Application Settings**: Update app settings for Function App and Web App
2. **Set Up AI Models**: Configure models in AI Foundry workspace
3. **Index Data**: Set up search indexes in Azure AI Search
4. **Configure Secrets**: Store connection strings and keys in Key Vault
5. **Set Up Monitoring**: Configure alerts and dashboards in Application Insights

## Security Considerations

- **Network Security**: All services configured with HTTPS-only access
- **Identity Management**: Uses Azure AD authentication where possible
- **Secret Management**: Connection strings stored in Key Vault
- **Access Control**: RBAC enabled for fine-grained permissions
- **Soft Delete**: Enabled for Key Vault and storage accounts

## Cost Management

- **Development**: Uses consumption/basic tiers for cost optimization
- **Staging**: Balances cost and performance for testing
- **Production**: Optimized for performance and availability
- **Monitoring**: Application Insights helps track resource usage

## Troubleshooting

### Common Issues

1. **Deployment Failures**
   - Check resource name uniqueness
   - Verify subscription quotas
   - Review error messages in deployment logs

2. **Permission Errors**
   - Ensure service principal has Contributor role
   - Check resource group permissions

3. **Resource Conflicts**
   - Verify resource names are globally unique
   - Check for existing resources with same names

### Cleanup

To remove all infrastructure:

```bash
# Delete resource group (removes all resources)
az group delete --name rg-agentic-ai-app-dev --yes --no-wait
```

## Support

For issues with infrastructure deployment:
1. Check GitHub Actions logs for deployment errors
2. Review Azure Activity Log for resource creation issues
3. Validate bicep templates locally before deployment
4. Ensure all prerequisites are met

## Next Steps

After infrastructure deployment:
1. Configure application deployments using CI/CD pipelines
2. Set up monitoring and alerting
3. Configure security policies and compliance
4. Scale resources based on usage patterns