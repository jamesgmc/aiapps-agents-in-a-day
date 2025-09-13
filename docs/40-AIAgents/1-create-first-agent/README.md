# First Agent in Foundry

:::info

Let's start to create our first agent in Foundry

:::

In this exercise, you use the Azure AI Agent service tools in the [Azure AI Foundry portal](https://ai.azure.com/) to create a agent for Flight Booking. The agent will be able to interact with users and provide information about flights.

## Access Azure AI Foundry

> **Note:** Azure AI Foundry was formerly known as Azure AI Studio.

1. We have provisioned an shared Foundry environment for you to use. Open the following link in your browser: [https://ai.azure.com/](https://ai.azure.com/) and sign in with your provided Azure lab account.
2. At home, you can follow these guidelines from the [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-studio/) blog post for creating an Azure AI Foundry hub yourself.
3. Azure AI Foundry portal should look like below:

    ![Azure AI Foundry Project](./images/azure-ai-foundry.png)

## Deploy a model

1. In the pane on the left for your project, in the **My assets** section, select the **Models + endpoints** page.
2. In the **Models + endpoints** page, in the **Model deployments** tab, in the **+ Deploy model** menu, select **Deploy base model**.
3. Search for the `gpt-4o` model in the list, and then select and confirm it. **We have deployed the gpt-4o model already, you can skip the actual creation step.***

    > **Note**: Reducing the TPM helps avoid over-using the quota available in the subscription you are using.

    ![Model Deployed](./images/model-deployment.png)

## Create an agent

Now that you have deployed a model, you can create an agent. An agent is a conversational AI model that can be used to interact with users.

1. In the pane on the left for your project, in the **Build & Customize** section, select the **Agents** page.
2. Click **+ Create agent** to create a new agent. Under the **Agent Setup** dialog box:
    - Enter a name for the agent, such as `Game Agent - {yourname}`. Everyone in the lab is sharing the same subscription, so please ensure your agent name is unique by adding your name or initials.
    - Ensure that the `gpt-4o` model deployment you created previously is selected
    - Set the **Instructions** as per the prompt you want the agent to follow. Here is an example:
    ```
    You are a Rock Paper Scissors agent. Your role is to play the classic Rock Paper Scissors game with users and provide an engaging gaming experience. Follow the instructions below to ensure clear and fun gameplay:

    ### Task Instructions:

    1. **Game Rules**: 
    - Rock beats Scissors
    - Scissors beats Paper
    - Paper beats Rock
    - Same choices result in a tie

    2. **Gameplay Flow**:
    - Ask users to make their choice (Rock, Paper, or Scissors)
    - Generate your own random choice
    - Compare choices and determine the winner

    3. **Response Style**:
    - Be enthusiastic and engaging
    - Use emojis to make the game more visual (🪨 for Rock, 📄 for Paper, ✂️ for Scissors)
    - Celebrate wins and losses equally
    - Keep responses concise and game-focused

    4. **Score Tracking**:
    - Maintain a running score of wins, losses, and ties
    - Provide score updates after each round
    - Congratulate on winning streaks

    Always stay in character as a fun, competitive Rock Paper Scissors game

    ```

> Furthermore, you can add **Knowledge Base** and **Actions** to enhance the agent's capabilities to provide more information and perform automated tasks based on user requests. For this exercise, you can skip these steps.
    
![Agent Setup](./images/agent-setup.png)


## Test the agent

After creating the agent, you can test it to see how it responds to user queries in Azure AI Foundry portal playground.

1. At the top of the **Setup** pane for your agent, select **Try in playground**.
2. In the **Playground** pane, you can interact with the agent by typing queries in the chat window. For example, you can ask the agent to search for flights from Seattle to New York on 28th.

    > **Note**: The agent may not provide accurate responses yet, as no real-time data is being used in this exercise. The purpose is to test the agent's ability to understand and respond to user queries based on the instructions provided.

    ![Agent Playground](./images/agent-playground.png)

3. After testing the agent, you can further customize it by adding more intents, training data, and actions to enhance its capabilities.

