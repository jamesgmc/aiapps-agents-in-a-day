# Agentic AI App in a Day (Lab)

## Lab Structure

### Part 1: Agentic AI Foundations & Prompt Engineering

- Introduction to agentic AI concepts (prompt → plan → act → reflect loop)
- Use Azure OpenAI for chat, planning, and coding
- Explore Semantic Kernel for agent memory and tool integration
- Hands-on: Build a simple agent that responds to prompts

### Part 2: Data Layer & Tool Integration

- Integrate Azure AI Search (RAG) for intelligent data retrieval
- Use Azure Functions for serverless tool integration
- Store agent state in Azure Storage or Cosmos DB
- Hands-on: Enhance the agent to use search and external tools

### Part 3: Orchestration & Deployment

- Orchestrate workflows with Azure Logic Apps
- Host the app using App Service, AKS, or Azure Container Apps
- Secure APIs with Azure API Management and manage secrets with Key Vault
- Hands-on: Deploy the agentic app, secure endpoints, and automate workflows

### Part 4: Multi-Agent Collaboration, and Production Readiness

- Enable multi-agent orchestration (agents collaborate, compete, or strategize)
- Prepare the app for production: security, scaling, and operational excellence

### Part 5: Scissor Paper Rock tournament
- Hands-on: Agents interact and compete in the "Scissor Paper Rock" game, demonstrating orchestration and monitoring


# Scissor Paper Rock Tournament:

API Server Design

Create an API server (Azure Functions or App Service) to manage tournament logic, player registration, and match orchestration.
Endpoints: register agent, start match, submit move, get results.
Agent Player Implementation

Each agent (player) connects to the API server, registers, and participates in matches.
Agents can be implemented as scripts or services (e.g., Python, Node.js).
Tournament Logic

8 players per group.
Each match: best of 3 rounds (first to 2 wins).
Winners advance to play other winners until a final winner is determined.
Azure Integration

Use Azure Functions for serverless API endpoints.
Store tournament state in Azure Storage or Cosmos DB.
Optionally, use Azure Logic Apps for orchestration.



# These topics to be covered in the lab:

Azure Resource Types
Azure AI Foundry (Model Catalog, Playground, Agent Service)
Azure OpenAI (LLMs for chat, planning, coding, summarization)
Azure AI Search (RAG, intelligent data layer)
Azure Functions (serverless tool integration)
Azure Logic Apps (workflow orchestration)
App Service / AKS / ACA (app hosting: web, container, Kubernetes)
Azure API Management (APIM) (secure API exposure)
Azure Key Vault (secrets management)
Azure Storage / Cosmos DB (agent state, knowledge storage)
Azure Monitor / Application Insights (logging, monitoring)
Technologies to Cover
Semantic Kernel (agent memory, planning, tool integration)
GitHub Copilot (coding assistant, automation)
Jupyter Notebooks (interactive exploration, model testing)
GitHub Codespaces (cloud dev environment)
Bicep (Infrastructure as Code for Azure)
Azure CLI / PowerShell (management, automation)
CI/CD (GitHub Actions, Azure DevOps for deployment)
Multi-Agent Orchestration (agent collaboration, perception → planning → action loop)
Security & Compliance (auth, rate limits, monitoring, cost controls)
Lab Focus Areas
Building agentic AI apps with prompt → plan → act → reflect loop
Integrating and orchestrating Azure AI services and tools
Deploying and operationalizing with containerization and CI/CD
Implementing security, monitoring, and production readiness




