---
title: Getting Started with AI Apps
slug: /40-AI-Apps-Setup
---

:::info LAB PRE-REQUISITES

- Access to the **AI Proxy Playground** (Use edge or chrome for the best experience)
- Azure OpenAI API Key
- VS Code
- Node.js and npm installed

:::

Welcome to the AI Apps Tutorial Series! In this lab, you'll learn to build practical AI-powered applications using Azure AI services. Each tutorial is designed as a guided, hands-on experience that builds real-world skills.

## What You'll Build

Through six comprehensive tutorials, you'll create AI applications that demonstrate:

1. **🎨 Design Generation** - Create visual concepts with DALL-E
2. **🌐 Translation Services** - Build multilingual customer support
3. **👁️ Computer Vision** - Analyze and understand images
4. **🗣️ Speech Processing** - Add voice capabilities to your apps
5. **🔍 SEO Automation** - Generate optimized content automatically
6. **🤖 Smart Automation** - Build intelligent workflow systems

## Tutorial Structure

Each tutorial follows a consistent structure:
- **Learning Objectives** - Clear goals for what you'll achieve
- **Scenario** - Real-world business context
- **Step-by-Step Implementation** - Guided coding experience
- **Solution Reference** - Complete working code examples
- **Best Practices** - Production-ready considerations
- **Integration Ideas** - Ways to extend and combine features

## AI Proxy Playground Setup

You'll be using a custom playground built on top of Azure OpenAI Service. This playground provides hands-on experience with AI APIs and helps you understand how to integrate them into applications.

**AI Proxy Playground:** https://arg-syd-aiaaa-playground.azurewebsites.net

### Authentication

1. Navigate to the AI Proxy Playground using the link provided during workshop registration
2. Enter your **API Key** in the top-right corner
3. Click `Authorize` to authenticate

### Explore the Interface

Once authenticated, you'll see:

- **Region 1️⃣** | User profile and session information
- **Region 2️⃣** | User prompt input for AI interactions
- **Region 3️⃣** | Conversation area with AI responses
- **Region 4️⃣** | Configuration panel with model settings
- **Region 5️⃣** | System message configuration
- **Region 6️⃣** | Function calling setup
- **Region 7️⃣** | Image generation (DALL-E) playground

## Development Environment Setup

### Prerequisites Check

Ensure you have the following installed:

```bash
# Check Node.js version (should be 16+ )
node --version

# Check npm version
npm --version

# Verify VS Code installation
code --version
```

### Chatbot Application

The tutorials use a React-based chatbot application located in `apps-chat/chatbot/`. This provides the UI framework for implementing AI features.

To set up the development environment:

```bash
# Navigate to the chatbot directory
cd apps-chat/chatbot

# Install dependencies
npm install

# Start the development server
npm run dev
```

The application will be available at `http://localhost:3000` with individual tutorial pages for each AI feature.

## Tutorial Navigation

### Beginner-Friendly Progression

The tutorials are designed to build upon each other:

1. **Start with Tutorial 1 (Design)** if you're new to AI APIs
2. **Focus on one tutorial at a time** to build understanding gradually
3. **Complete the implementation** before moving to the next tutorial
4. **Experiment with the advanced features** to deepen your knowledge

### Independent Learning

Each tutorial can also be completed independently if you have specific interests:

- **Visual AI** → Tutorials 1 (Design) and 3 (Vision)
- **Language AI** → Tutorials 2 (Translation) and 5 (SEO)
- **Conversational AI** → Tutorials 4 (Speech) and 6 (Automation)

## Tips for Success

### 1. Select the Right Model

Different tutorials use different AI models:
- **GPT-4o** for text and vision tasks
- **DALL-E 3** for image generation
- **Azure Speech Services** for text-to-speech

Always select the appropriate model in the Configuration section before testing.

### 2. Clear Chat Sessions

Each tutorial involves different prompts and contexts. Click "Clear Chat" between different tutorial exercises to ensure clean results.

### 3. Copy-Paste Code Snippets

Tutorial code is provided in copy-friendly format. Click the copy icon in code blocks to quickly transfer code to your development environment.

```typescript
// Example: This code block has a copy button
async function exampleFunction() {
    console.log("Ready to start building AI apps!");
}
```

### 4. Incremental Development

- **Test each function** as you implement it
- **Use console.log** to debug API responses
- **Start simple** and add complexity gradually
- **Refer to solution code** when you get stuck

## What's Next?

Ready to start building? Head to **Tutorial 1: Product Design with DALL-E** to begin your AI app development journey!

Each tutorial builds practical skills you can apply immediately in real-world projects. By the end of this series, you'll have a comprehensive understanding of how to integrate multiple AI services into production applications.

---

:::tip REMEMBER
- Keep your API keys secure
- Test thoroughly before deploying
- Consider rate limits and costs
- Build with user experience in mind
:::
