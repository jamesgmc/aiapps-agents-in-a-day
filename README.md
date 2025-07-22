# Agentic AI App in a Day

## Presentation #1: Morning, Kick-start – 30 min
**Topics:** Basic Concepts and Overview
- Azure AI + Agentic AI overview  
- Agentic AI design patterns (Planning, Tool Use, Reflection, Multi-agent)  
- Agent architectures: ReAct, Chain-of-Thought
- Memory systems for agents (short-term, long-term, episodic)
- Tool integration patterns and API orchestration
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
**Topic:** Building Production-Ready AI Apps with Agentic Concepts
- Technical Deep Dive: Advanced reasoning architectures and hybrid - approaches for complex problem-solving
- Practical Considerations: Memory, cost, performance optimization - and error handling strategies
- Enterprise Readiness: Security, evaluation, testing, and compliance frameworks for production deployment
- Platform-First Strategies: Scaling, API management, DevOps, and platform selection best practices
- Real-World Implementation Patterns: Customer service, document processing, developer tools, and multi-modal applications


## Lab #3: AI Agent 101 & Sementic Kernal
**Build an agent**
- Prompt → Plan → Act → Reflect loop  
- Basic tool usage and chaining outputs  
- Setup Codespaces + sample agent repo

## Demo #2: Multi-Agent Walkthrough
**:**
- Show multi-agent collaboration, perception → planning → action loop
- Real-world scenario (Daniel's LEGO demo)  

## Demo #3: Agent Mode Coding Assistant for AI App
**Developer experience showcase:**
- Prompt-driven coding assistant (e.g., auto-generate unit tests, fix bugs)  
- Refactoring, adding comments/images, reformatting examples  
- Show how devs stay in control but move faster

## Lab #4: Deployment + API Layer
**Deploy and expose app:**
- Containerize the agent app
- Deploy ai app and integration to Azure
- Expose via Azure API Management (with auth, rate limits, monitoring)

## Presentation #3: Afternoon – 30 min
**Topic:** Responsible AI & Future Considerations

- Responsible AI and Guiderails: Content filtering, prompt injection defense, evaluation, and monitoring
- Observability & Operations: Agent analytics, performance metrics, cost tracking, and debugging
- Advanced Topics & Future Trends: Fine-tuning, multi-modal agents, edge deployment, and emerging frameworks
- Lessons Learned & Best Practices: Common pitfalls, testing strategies, and migration patterns
- Next Steps & Resources: Certification paths, community support, and building your first production agent


## Azure Services & Framework to be considered
- **Azure OpenAI** – LLMs for chat, planning, coding, summarization  
- **Azure AI Foundry (Model Catalog, Playground)** – To explore and test models  
- **Azure AI Foundry – Agent Service** – For orchestrating multi-agent systems  
- **Azure AI Services** – For integrating vision, speech, etc.  
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

