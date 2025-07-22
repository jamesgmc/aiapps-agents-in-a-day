# Agentic AI App in a Day

## Presentation #1: Morning, Kick-start – 30 min
**Topics:** Basic Concepts and Overview
- Azure AI + Agentic AI overview  
- Agentic design patterns (Planning, Tool Use, Reflection, Multi-agent)  
- Intelligent data layers (Azure Cognitive Search, RAG)  

## Lab #1: Foundry Integration & Extension
**Leverage Azure AI Foundry services:**
- Use Model Catalog and various Azure AI Services
- Customize agent orchestration using no-code / low-code blocks  
- Connect additional tools (e.g., a calculator API, web search API)

## Demo #1: Using an Accelerator Repo
- Multi-agent orchestration using Azure AI Foundry Agent Service

## Lab #2: Add Intelligent Data Layer
**Integrate Azure AI Search (RAG):**
- Ingest doc into Azure AI Search
- Use Document Intelligence Service
- Connect agent to knowledge base  
- Demonstrate contextual reasoning  
- Optional: Build a memory/retrieval plugin with Semantic Kernel

## Presentation #2: After Lunch – 30 min
**Topic:** Platform-first strategies  
- Scaling with AKS / ACA  
- Secure APIs with APIM  
- DevOps mindset and governance  
- Foundry vs. DIY orchestration considerations

## Lab #3: AI Agent 101 & Sementic Kernal
**Build a simple agent in Codespaces:**
- Prompt → Plan → Act → Reflect loop  
- Basic tool usage and chaining outputs  
- Setup Codespaces + sample agent repo

## Demo #2: Multi-Agent Walkthrough
**:**
- Real-world scenario (Daniel's LEGO demo)  
- Show multi-agent collaboration, perception → planning → action loop

## Demo #3: Agent Mode Coding Assistant for AI App
**Developer experience showcase:**
- Prompt-driven coding assistant (e.g., auto-generate unit tests, fix bugs)  
- Refactoring, adding comments/images, reformatting examples  
- Show how devs stay in control but move faster

## Lab #4: Deployment + API Layer
**Deploy and expose app:**
- Containerize the agent app
- Deploy to AKS or Azure Container Apps  
- Expose via Azure API Management (with auth, rate limits, monitoring)  

## Presentation #3: Afternoon – 30 min
**Topic:** Responsible AI  
- Azure OpenAI Content Filters, Prompt injection defense  
- Evaluation techniques (Foundry red teaming tools, logs)  
- API-level protections (input validation via APIM)  
- Monitoring & transparency, audit logs


## Azure Services to be considered
- **Azure OpenAI** – LLMs for chat, planning, coding, summarization  
- **Azure AI Foundry (Model Catalog, Playground)** – To explore and test models  
- **Azure AI Foundry – Agent Service** – For orchestrating multi-agent systems  
- **Azure AI Foundry – Azure AI Services** – For integrating vision, speech, etc.  
- **Semantic Kernel** – For agent memory, function calling, planning  
- **App service / AKS / ACA** – App hosting  
- **APIM** – Secure, scalable API layer
- **Azure AI Search** – Intelligent data layer for RAG
- **Azure Functions** – Serverless compute for tool integration
- **Azure Logic Apps** – Workflow automation for tool orchestration
- **Azure DevOps / GitHub Actions** – CI/CD for agent apps
- **Azure Monitor / Application Insights** – Monitoring and logging
- **Azure Key Vault** – Secure secrets management
- **Azure Storage / Cosmos DB** – Data storage for agent state and knowledge

## Lab Exercise to be considered

https://github.com/Azure-Samples/AI-Gateway

## Accelerator Repo to be considered
- https://github.com/Azure-Samples/get-started-with-ai-chat
- https://github.com/Azure-Samples/get-started-with-ai-agents
- https://github.com/microsoft/Multi-Agent-Custom-Automation-Engine-Solution-Accelerator
- https://github.com/microsoft/content-processing-solution-accelerator
- https://github.com/microsoft/document-generation-solution-accelerator
- https://github.com/microsoft/Build-your-own-copilot-Solution-Accelerator
- https://github.com/microsoft/Modernize-your-code-solution-accelerator
- https://github.com/Azure-Samples/Azure-Language-OpenAI-Conversational-Agent-Accelerator
- https://github.com/microsoft/Conversation-Knowledge-Mining-Solution-Accelerator

