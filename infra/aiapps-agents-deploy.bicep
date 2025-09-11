// Main bicep template for AI Apps and Agents infrastructure
@description('Location for all resources')
param location string = resourceGroup().location

@description('Application name prefix')
param appName string = 'aiapps-agents'

@description('Unique suffix for resource names')
param uniqueSuffix string = uniqueString(resourceGroup().id)

// Variables
var resourcePrefix = '${appName}'
var storageAccountName = replace('${resourcePrefix}st${uniqueSuffix}', '-', '')
var keyVaultName = '${resourcePrefix}-kv-${uniqueSuffix}'
var cosmosDbAccountName = '${resourcePrefix}-cosmos-${uniqueSuffix}'
var searchServiceName = '${resourcePrefix}-search-${uniqueSuffix}'
var appInsightsName = '${resourcePrefix}-ai-${uniqueSuffix}'
var logAnalyticsName = '${resourcePrefix}-la-${uniqueSuffix}'
var acrName = replace('${resourcePrefix}acr${uniqueSuffix}', '-', '')
var functionAppName = '${resourcePrefix}-func-${uniqueSuffix}'
var logicAppName = '${resourcePrefix}-logic-${uniqueSuffix}'
var webAppName = '${resourcePrefix}-webapp-${uniqueSuffix}'
var staticWebAppName = '${resourcePrefix}-swa-${uniqueSuffix}'
var aiFoundryWorkspaceName = '${resourcePrefix}-ai-workspace-${uniqueSuffix}'
// var aiFoundryProjectName = '${resourcePrefix}-ai-project-${uniqueSuffix}' // Reserved for future AI project creation

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

// Cosmos DB Account
resource cosmosDbAccount 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: cosmosDbAccountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    enableFreeTier: false
    databaseAccountOfferType: 'Standard'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: [
      {
        name: 'EnableServerless'
      }
    ]
    backupPolicy: {
      type: 'Periodic'
      periodicModeProperties: {
        backupIntervalInMinutes: 240
        backupRetentionIntervalInHours: 8
        backupStorageRedundancy: 'Local'
      }
    }
  }
}

// Azure AI Search
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: searchServiceName
  location: location
  sku: {
    name: 'basic'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    publicNetworkAccess: 'enabled'
    networkRuleSet: {
      ipRules: []
    }
    encryptionWithCmk: {
      enforcement: 'Unspecified'
    }
    disableLocalAuth: false
    authOptions: {
      apiKeyOnly: {}
    }
  }
}

// Azure Container Registry
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: acrName
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
    policies: {
      quarantinePolicy: {
        status: 'disabled'
      }
      trustPolicy: {
        type: 'Notary'
        status: 'disabled'
      }
      retentionPolicy: {
        days: 7
        status: 'disabled'
      }
      exportPolicy: {
        status: 'enabled'
      }

    }
    encryption: {
      status: 'disabled'
    }
    dataEndpointEnabled: false
    publicNetworkAccess: 'Enabled'
    networkRuleBypassOptions: 'AzureServices'
    zoneRedundancy: 'Disabled'

  }
}

// App Service Plan for Function App and Web App
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${resourcePrefix}-asp-${uniqueSuffix}'
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
    size: 'Y1'
    family: 'Y'
    capacity: 0
  }
  properties: {
    perSiteScaling: false
    elasticScaleEnabled: false
    maximumElasticWorkerCount: 1
    isSpot: false
    reserved: false
    isXenon: false
    hyperV: false
    targetWorkerCount: 0
    targetWorkerSizeId: 0
    zoneRedundant: false
  }
}

// App Service Plan for Web App (separate plan for different SKU)
resource webAppServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${resourcePrefix}-webapp-asp-${uniqueSuffix}'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
    size: 'B1'
    family: 'B'
    capacity: 1
  }
  properties: {
    perSiteScaling: false
    elasticScaleEnabled: false
    maximumElasticWorkerCount: 1
    isSpot: false
    reserved: false
    isXenon: false
    hyperV: false
    targetWorkerCount: 0
    targetWorkerSizeId: 0
    zoneRedundant: false
  }
}

// Azure Function App
resource functionApp 'Microsoft.Web/sites@2022-09-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp'
  properties: {
    enabled: true
    hostNameSslStates: [
      {
        name: '${functionAppName}.azurewebsites.net'
        sslState: 'Disabled'
        hostType: 'Standard'
      }
      {
        name: '${functionAppName}.scm.azurewebsites.net'
        sslState: 'Disabled'
        hostType: 'Repository'
      }
    ]
    serverFarmId: appServicePlan.id
    reserved: false
    isXenon: false
    hyperV: false
    vnetRouteAllEnabled: false
    vnetImagePullEnabled: false
    vnetContentShareEnabled: false
    siteConfig: {
      numberOfWorkers: 1
      acrUseManagedIdentityCreds: false
      alwaysOn: false
      http20Enabled: false
      functionAppScaleLimit: 200
      minimumElasticInstanceCount: 0
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${az.environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};EndpointSuffix=${az.environment().suffixes.storage};AccountKey=${storageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(functionAppName)
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'dotnet'
        }
      ]
    }
    scmSiteAlsoStopped: false
    clientAffinityEnabled: false
    clientCertEnabled: false
    clientCertMode: 'Required'
    hostNamesDisabled: false
    customDomainVerificationId: 'D6F2F0173FF3C1601E5D703C2B40F9D8BC8D7E84E5A75F17C9E6F7B8E5D703C2'
    containerSize: 1536
    dailyMemoryTimeQuota: 0
    httpsOnly: true
    redundancyMode: 'None'
    storageAccountRequired: false
    keyVaultReferenceIdentity: 'SystemAssigned'
  }
}

// Azure Web App for Game Server
resource webApp 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  kind: 'app'
  properties: {
    enabled: true
    hostNameSslStates: [
      {
        name: '${webAppName}.azurewebsites.net'
        sslState: 'Disabled'
        hostType: 'Standard'
      }
      {
        name: '${webAppName}.scm.azurewebsites.net'
        sslState: 'Disabled'
        hostType: 'Repository'
      }
    ]
    serverFarmId: webAppServicePlan.id
    reserved: false
    isXenon: false
    hyperV: false
    vnetRouteAllEnabled: false
    vnetImagePullEnabled: false
    vnetContentShareEnabled: false
    siteConfig: {
      numberOfWorkers: 1
      acrUseManagedIdentityCreds: false
      alwaysOn: true
      http20Enabled: false
      appSettings: [
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
      ]
      netFrameworkVersion: 'v8.0'
    }
    scmSiteAlsoStopped: false
    clientAffinityEnabled: true
    clientCertEnabled: false
    clientCertMode: 'Required'
    hostNamesDisabled: false
    customDomainVerificationId: 'D6F2F0173FF3C1601E5D703C2B40F9D8BC8D7E84E5A75F17C9E6F7B8E5D703C2'
    containerSize: 0
    dailyMemoryTimeQuota: 0
    httpsOnly: true
    redundancyMode: 'None'
    storageAccountRequired: false
    keyVaultReferenceIdentity: 'SystemAssigned'
  }
}

// Azure Logic App
resource logicApp 'Microsoft.Logic/workflows@2019-05-01' = {
  name: logicAppName
  location: location
  properties: {
    state: 'Enabled'
    definition: {
      '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#'
      contentVersion: '1.0.0.0'
      parameters: {}
      triggers: {
        manual: {
          type: 'Request'
          kind: 'Http'
          inputs: {
            schema: {}
          }
        }
      }
      actions: {
        Response: {
          type: 'Response'
          inputs: {
            statusCode: 200
            body: 'Hello from Logic App!'
          }
          runAfter: {}
        }
      }
      outputs: {}
    }
    parameters: {}
  }
}

// Static Web App
resource staticWebApp 'Microsoft.Web/staticSites@2022-09-01' = {
  name: staticWebAppName
  location: 'EastUS2'
  sku: {
    name: 'Free'
    tier: 'Free'
    size: 'Free'
    family: 'Free'
    capacity: 0
  }
  properties: {
    repositoryUrl: ''
    branch: ''
    buildProperties: {
      appLocation: '/apps-rps/rps-game-client'
      apiLocation: ''
      outputLocation: 'dist'
    }
    stagingEnvironmentPolicy: 'Enabled'
    allowConfigFileUpdates: true
    provider: 'None'
    enterpriseGradeCdnStatus: 'Disabled'
  }
}

// AI Foundry Workspace (Azure Machine Learning workspace)
resource aiFoundryWorkspace 'Microsoft.MachineLearningServices/workspaces@2023-08-01-preview' = {
  name: aiFoundryWorkspaceName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: aiFoundryWorkspaceName
    description: 'AI Foundry workspace for AI Apps and Agents'
    storageAccount: storageAccount.id
    keyVault: keyVault.id
    applicationInsights: appInsights.id
    containerRegistry: containerRegistry.id
    publicNetworkAccess: 'Enabled'
    imageBuildCompute: 'cpu-cluster'
    allowPublicAccessWhenBehindVnet: false
    discoveryUrl: 'https://${location}.api.azureml.ms/discovery'
    v1LegacyMode: false
  }
  kind: 'Hub'
}

// AI Foundry Project (Azure Machine Learning Project)
var aiFoundryProjectName = '${resourcePrefix}-ai-project-${uniqueSuffix}'
resource aiFoundryProject 'Microsoft.MachineLearningServices/projects@2023-08-01-preview' = {
  name: aiFoundryProjectName
  location: location
  properties: {
    workspaceId: aiFoundryWorkspace.id
    description: 'AI Foundry project for AI Apps and Agents'
    friendlyName: aiFoundryProjectName
    publicNetworkAccess: 'Enabled'
  }
}

// Outputs
output resourceGroupName string = resourceGroup().name
output storageAccountName string = storageAccount.name
output keyVaultName string = keyVault.name
output cosmosDbAccountName string = cosmosDbAccount.name
output searchServiceName string = searchService.name
output appInsightsName string = appInsights.name
output acrName string = containerRegistry.name
output functionAppName string = functionApp.name
output webAppName string = webApp.name
output logicAppName string = logicApp.name
output staticWebAppName string = staticWebApp.name
output aiFoundryWorkspaceName string = aiFoundryWorkspace.name
// output storageAccountKey string = storageAccount.listKeys().keys[0].value // Removed to avoid exposing secrets in outputs
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output appInsightsConnectionString string = appInsights.properties.ConnectionString
