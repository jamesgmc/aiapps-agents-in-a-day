// Main bicep template for AI Apps and Agents infrastructure
@description('Location for all resources')
param location string = 'eastus'

@description('Application name prefix')
param appName string = 'aiapps-agents'

@description('Unique suffix for resource names')
param uniqueSuffix string = uniqueString(resourceGroup().id)

@description('Specifies the SKU for the Azure App Service plan. Defaults to **S1**')
param appServiceSku string = 'S1'

@description('Specifies the SKU for the Azure OpenAI resource. Defaults to **S0**')
param openAiSku string = 'S0'

@description('MongoDB vCore user Name. No dashes.')
param mongoDbUserName string

@description('MongoDB vCore password. 8-256 characters, 3 of the following: lower case, upper case, numeric, symbol.')
@secure()
param mongoDbPassword string

// Variables
var resourcePrefix = appName
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
var openAiName = '${resourcePrefix}-openai-${uniqueSuffix}'
var mongoClusterName = '${resourcePrefix}-mongo-${uniqueSuffix}'

// OpenAI model configurations
var openAiSettings = {
  name: openAiName
  sku: openAiSku
  maxConversationTokens: '100'
  maxCompletionTokens: '500'
  gptModel: {
    name: 'gpt-4o'
    version: '2024-05-13'
    deployment: {
      name: 'gpt4o'
    }
    sku: {
      name: 'Standard'
      capacity: 300
    }
  }
  completionsModel: {
    name: 'gpt-4o'
    version: '2024-05-13'
    deployment: {
      name: 'completions'
    }
    sku: {
      name: 'Standard'
      capacity: 300
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
      capacity: 300
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

// MongoDB cluster settings
var mongovCoreSettings = {
  mongoClusterName: mongoClusterName
  mongoClusterLogin: mongoDbUserName
  mongoClusterPassword: mongoDbPassword
}

// App service settings
var appServiceSettings = {
  plan: {
    name: '${resourcePrefix}-web'
    sku: appServiceSku
  }
  playground: {
    name: '${resourcePrefix}-playground'
  }
  api: {
    name: '${resourcePrefix}-api'
  }
  chat: {
    name: '${resourcePrefix}-chat'
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
// AI Apps
// -----------------------

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

// MongoDB vCore Cluster
resource mongoCluster 'Microsoft.DocumentDB/mongoClusters@2023-03-01-preview' = {
  name: mongovCoreSettings.mongoClusterName
  location: location
  properties: {
    administratorLogin: mongovCoreSettings.mongoClusterLogin
    administratorLoginPassword: mongovCoreSettings.mongoClusterPassword
    serverVersion: '5.0'
    nodeGroupSpecs: [
      {
        kind: 'Shard'
        sku: 'M30'
        diskSizeGB: 128
        enableHa: false
        nodeCount: 1
      }
    ]
  }
}

resource mongoFirewallRulesAllowAzure 'Microsoft.DocumentDB/mongoClusters/firewallRules@2023-03-01-preview' = {
  parent: mongoCluster
  name: 'allowAzure'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

resource mongoFirewallRulesAllowAll 'Microsoft.DocumentDB/mongoClusters/firewallRules@2023-03-01-preview' = {
  parent: mongoCluster
  name: 'allowAll'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '255.255.255.255'
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

resource openAiGpt4oModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAiAccount
  name: openAiSettings.gptModel.deployment.name
  dependsOn: [
    openAiEmbeddingsModelDeployment
  ]
  sku: {
    name: openAiSettings.gptModel.sku.name
    capacity: openAiSettings.gptModel.sku.capacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: openAiSettings.gptModel.name
      version: openAiSettings.gptModel.version
    }    
  }
}

resource openAiCompletionsModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAiAccount
  name: openAiSettings.completionsModel.deployment.name
  dependsOn: [
    openAiEmbeddingsModelDeployment
    openAiGpt4oModelDeployment
  ]
  sku: {
    name: openAiSettings.completionsModel.sku.name
    capacity: openAiSettings.completionsModel.sku.capacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: openAiSettings.completionsModel.name
      version: openAiSettings.completionsModel.version
    }    
  }
}

resource openAiDalleModelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAiAccount
  name: openAiSettings.dalleModel.deployment.name
  dependsOn: [
    openAiEmbeddingsModelDeployment
    openAiCompletionsModelDeployment
    openAiGpt4oModelDeployment
  ]
  sku: {
    name: openAiSettings.dalleModel.sku.name
    capacity: openAiSettings.dalleModel.sku.capacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: openAiSettings.dalleModel.name
      version: openAiSettings.dalleModel.version
    }    
  }
}

// Computer Vision Service
resource computerVision 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${resourcePrefix}-cv-${uniqueSuffix}'
  location: location
  kind: 'ComputerVision'
  properties: {
    customSubDomainName: '${resourcePrefix}-cv-${uniqueSuffix}'
    publicNetworkAccess: 'Enabled'
  }
  sku: {
    name: 'S1'
  }
}

// Speech Service
resource speechService 'Microsoft.CognitiveServices/accounts@2021-04-30' = {
  name: '${resourcePrefix}-speech-${uniqueSuffix}'
  location: location
  kind: 'SpeechServices'
  sku: {
    name: 'S0'
  }
  properties: {
    apiProperties: {
      qnaRuntimeEndpoint: 'https://${resourcePrefix}-speech-${uniqueSuffix}.api.cognitive.microsoft.com'
    }
  }
}

// Translator Service
resource translatorService 'Microsoft.CognitiveServices/accounts@2021-04-30' = {
  name: '${resourcePrefix}-translator-${uniqueSuffix}'
  location: location
  kind: 'TextTranslation'
  sku: {
    name: 'S1'
  }
  properties: {
    apiProperties: {
      qnaRuntimeEndpoint: 'https://${resourcePrefix}-translator-${uniqueSuffix}.api.cognitive.microsoft.com'
    }
  }
}



// Additional App Services from azuredeploy.bicep
resource appServicePlanLinux 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: '${appServiceSettings.plan.name}-asp'
  location: location
  sku: {
    name: appServiceSettings.plan.sku
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource appServicePlayground 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceSettings.playground.name
  location: location
  properties: {
    serverFarmId: appServicePlanLinux.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      appCommandLine: 'pm2 serve /home/site/wwwroot/dist --no-daemon --spa'
      alwaysOn: true
    }
  }
}

resource appServicePlaygroundSettings 'Microsoft.Web/sites/config@2022-03-01' = {
  parent: appServicePlayground
  name: 'appsettings'
  kind: 'string'
  properties: {
    APPINSIGHTS_INSTRUMENTATIONKEY: appInsights.properties.InstrumentationKey
  }
}

resource appServiceApi 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceSettings.api.name
  location: location
  properties: {
    serverFarmId: appServicePlanLinux.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      appCommandLine: 'pm2 start app.js --no-daemon'
      alwaysOn: true
    }
  }
}

resource appServiceApiSettings 'Microsoft.Web/sites/config@2022-03-01' = {
  parent: appServiceApi
  name: 'appsettings'
  kind: 'string'
  properties: {
    APPINSIGHTS_INSTRUMENTATIONKEY: appInsights.properties.InstrumentationKey
  }
}

resource appServiceChat 'Microsoft.Web/sites@2022-03-01' = {
  name: appServiceSettings.chat.name
  location: location
  properties: {
    serverFarmId: appServicePlanLinux.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      appCommandLine: 'pm2 serve /home/site/wwwroot/dist --no-daemon --spa'
      alwaysOn: true
    }
  }
}

resource appServiceChatSettings 'Microsoft.Web/sites/config@2022-03-01' = {
  parent: appServiceChat
  name: 'appsettings'
  kind: 'string'
  properties: {
    APPINSIGHTS_INSTRUMENTATIONKEY: appInsights.properties.InstrumentationKey
  }
}

// -----------------------
// AI Agents
// -----------------------

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
output mongoClusterName string = mongoCluster.name
output openAiAccountName string = openAiAccount.name
output computerVisionName string = computerVision.name
output speechServiceName string = speechService.name
output translatorServiceName string = translatorService.name
output playgroundAppName string = appServicePlayground.name
output apiAppName string = appServiceApi.name
output chatAppName string = appServiceChat.name
output searchServiceName string = searchService.name
output appInsightsName string = appInsights.name
output acrName string = containerRegistry.name
output functionAppName string = functionApp.name
output webAppName string = webApp.name
output logicAppName string = logicApp.name
output staticWebAppName string = staticWebApp.name
output aiFoundryWorkspaceName string = aiFoundryWorkspace.name
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
output appInsightsConnectionString string = appInsights.properties.ConnectionString
