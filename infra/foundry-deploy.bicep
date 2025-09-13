// Main bicep template for AI Apps and Agents infrastructure
@description('Location for all resources')
param location string = 'eastus'

@description('Application name prefix')
param appName string = 'aiapps-agents'

// Variables
var resourceGroupName = resourceGroup().name
// Create a suffix using the last part of the resource group name, safely handling short names
var resourceGroupSuffix = take(replace(guid(resourceGroupName), '-', ''), 6)
var resourcePrefix = appName
var logAnalyticsName = '${resourcePrefix}-logs-${resourceGroupSuffix}'
var appInsightsName = '${resourcePrefix}-ai-${resourceGroupSuffix}'
var storageAccountName = replace('${resourcePrefix}st${resourceGroupSuffix}', '-', '')
var keyVaultName = '${resourcePrefix}-kv-${resourceGroupSuffix}'

// Web app service names
var openAiName = '${resourcePrefix}-openai-${resourceGroupSuffix}'


// OpenAI model configurations
var openAiSettings = {
  name: openAiName
  sku: 'S0'
  maxConversationTokens: '100'
  maxCompletionTokens: '500'
  gptModel: {
    name: 'gpt-4o'
    version: '2024-05-13'
    deployment: {
      name: 'gpt-4o'
    }
    sku: {
      name: 'Standard'
      capacity: 50
    }
  }
  embeddingsModel: {
    name: 'text-embedding-3-small'
    version: '1'
    deployment: {
      name: 'embeddings'
    }
    sku: {
      name: 'Standard'
      capacity: 50
    }
  }
  dalleModel: {
    name: 'dall-e-3'
    version: '3.0'
    deployment: {
      name: 'dalle3'
    }
    sku: {
      name: 'Standard'
      capacity: 1
    }
  }
}



// Log Analytics Workspace (required for Application Insights)
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
    features: {
      enableLogAccessUsingOnlyResourcePermissions: true
    }
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    defaultToOAuthAuthentication: false
    allowCrossTenantReplication: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    allowSharedKeyAccess: true
    networkAcls: {
      bypass: 'AzureServices'
      virtualNetworkRules: []
      ipRules: []
      defaultAction: 'Allow'
    }
    supportsHttpsTrafficOnly: true
    encryption: {
      requireInfrastructureEncryption: false
      services: {
        file: {
          keyType: 'Account'
          enabled: true
        }
        blob: {
          keyType: 'Account'
          enabled: true
        }
      }
      keySource: 'Microsoft.Storage'
    }
    accessTier: 'Hot'
  }
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    accessPolicies: []
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enableRbacAuthorization: true
    provisioningState: 'Succeeded'
    publicNetworkAccess: 'Enabled'
  }
}


// -----------------------
// AI Services
// -----------------------

// Azure AI Foundry Workspace (formerly ML Services)
resource aiFoundryWorkspace 'Microsoft.MachineLearningServices/workspaces@2025-07-01-preview' = {
  name: '${resourcePrefix}-foundry-${resourceGroupSuffix}'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: 'AI Foundry Workspace for ${appName}'
    description: 'Azure AI Foundry workspace for building AI applications'
    keyVault: keyVault.id
    storageAccount: storageAccount.id
    applicationInsights: appInsights.id
    publicNetworkAccess: 'Enabled'
    hbiWorkspace: false
    v1LegacyMode: false
    systemDatastoresAuthMode: 'Identity'
    managedNetwork: {
      isolationMode: 'Disabled'
    }
  }
}

// Azure OpenAI Service
resource openAiAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAiSettings.name
  location: location
  sku: {
    name: openAiSettings.sku    
  }
  kind: 'OpenAI'
  properties: {
    customSubDomainName: openAiSettings.name
    publicNetworkAccess: 'Enabled'
  }
}

resource openAiEmbeddingsModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAiAccount
  name: openAiSettings.embeddingsModel.deployment.name  
  sku: {
    name: openAiSettings.embeddingsModel.sku.name
    capacity: openAiSettings.embeddingsModel.sku.capacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: openAiSettings.embeddingsModel.name
      version: openAiSettings.embeddingsModel.version
    }
  }
}

// resource openAiGpt4oModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
//   parent: openAiAccount
//   name: openAiSettings.gptModel.deployment.name
//   dependsOn: [
//     openAiEmbeddingsModelDeployment
//   ]
//   sku: {
//     name: openAiSettings.gptModel.sku.name
//     capacity: openAiSettings.gptModel.sku.capacity
//   }
//   properties: {
//     model: {
//       format: 'OpenAI'
//       name: openAiSettings.gptModel.name
//       version: openAiSettings.gptModel.version
//     }    
//   }
// }


// resource openAiDalleModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
//   parent: openAiAccount
//   name: openAiSettings.dalleModel.deployment.name
//   dependsOn: [
//     openAiEmbeddingsModelDeployment
//     // openAiGpt4oModelDeployment
//   ]
//   sku: {
//     name: openAiSettings.dalleModel.sku.name
//     capacity: openAiSettings.dalleModel.sku.capacity
//   }
//   properties: {
//     model: {
//       format: 'OpenAI'
//       name: openAiSettings.dalleModel.name
//       version: openAiSettings.dalleModel.version
//     }    
//   }
// }

// Computer Vision Service
resource computerVision 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${resourcePrefix}-cv-${resourceGroupSuffix}'
  location: location
  kind: 'ComputerVision'
  properties: {
    customSubDomainName: '${resourcePrefix}-cv-${resourceGroupSuffix}'
    publicNetworkAccess: 'Enabled'
  }
  sku: {
    name: 'S1'
  }
}

// Speech Service
resource speechService 'Microsoft.CognitiveServices/accounts@2021-04-30' = {
  name: '${resourcePrefix}-speech-${resourceGroupSuffix}'
  location: location
  kind: 'SpeechServices'
  sku: {
    name: 'S0'
  }
  properties: {
    apiProperties: {
      qnaRuntimeEndpoint: 'https://${resourcePrefix}-speech-${resourceGroupSuffix}.api.cognitive.microsoft.com'
    }
  }
}

// Translator Service
resource translatorService 'Microsoft.CognitiveServices/accounts@2021-04-30' = {
  name: '${resourcePrefix}-translator-${resourceGroupSuffix}'
  location: location
  kind: 'TextTranslation'
  sku: {
    name: 'S1'
  }
  properties: {
    apiProperties: {
      qnaRuntimeEndpoint: 'https://${resourcePrefix}-translator-${resourceGroupSuffix}.api.cognitive.microsoft.com'
    }
  }
}

