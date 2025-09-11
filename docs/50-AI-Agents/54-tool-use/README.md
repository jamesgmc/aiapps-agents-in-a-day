
# Tool Use Design Pattern

//todo: for game agent, add tool use, call it agent_v54.py in apps-rps/rps-game-agent. follow agent_v1.py

Tools are interesting because they allow AI agents to have a broader range of capabilities. Instead of the agent having a limited set of actions it can perform, by adding a tool, the agent can now perform a wide range of actions. In this chapter, we will look at the Tool Use Design Pattern, which describes how AI agents can use specific tools to achieve their goals.

## What is the Tool Use Design Pattern?

The **Tool Use Design Pattern** focuses on giving LLMs the ability to interact with external tools to achieve specific goals. Tools are code that can be executed by an agent to perform actions. A tool can be a simple function such as a calculator, or an API call to a third-party service such as stock price lookup or weather forecast. In the context of AI agents, tools are designed to be executed by agents in response to **model-generated function calls**.

## What are the use cases it can be applied to?

AI Agents can leverage tools to complete complex tasks, retrieve information, or make decisions. The tool use design pattern is often used in scenarios requiring dynamic interaction with external systems, such as databases, web services, or code interpreters. This ability is useful for a number of different use cases including:

- **Dynamic Information Retrieval:** Agents can query external APIs or databases to fetch up-to-date data (e.g., querying a SQLite database for data analysis, fetching stock prices or weather information).
- **Code Execution and Interpretation:** Agents can execute code or scripts to solve mathematical problems, generate reports, or perform simulations.
- **Workflow Automation:** Automating repetitive or multi-step workflows by integrating tools like task schedulers, email services, or data pipelines.
- **Customer Support:** Agents can interact with CRM systems, ticketing platforms, or knowledge bases to resolve user queries.
- **Content Generation and Editing:** Agents can leverage tools like grammar checkers, text summarizers, or content safety evaluators to assist with content creation tasks.

## What are the elements/building blocks needed to implement the tool use design pattern?

These building blocks allow the AI agent to perform a wide range of tasks. Let's look at the key elements needed to implement the Tool Use Design Pattern:

- **Function/Tool Schemas**: Detailed definitions of available tools, including function name, purpose, required parameters, and expected outputs. These schemas enable the LLM to understand what tools are available and how to construct valid requests.

- **Function Execution Logic**: Governs how and when tools are invoked based on the user’s intent and conversation context. This may include planner modules, routing mechanisms, or conditional flows that determine tool usage dynamically.

- **Message Handling System**: Components that manage the conversational flow between user inputs, LLM responses, tool calls, and tool outputs.

- **Tool Integration Framework**: Infrastructure that connects the agent to various tools, whether they are simple functions or complex external services.

- **Error Handling & Validation**: Mechanisms to handle failures in tool execution, validate parameters, and manage unexpected responses.

- **State Management**: Tracks conversation context, previous tool interactions, and persistent data to ensure consistency across multi-turn interactions.

Next, let's look at Function/Tool Calling in more detail.
 
### Function/Tool Calling

Function calling is the primary way we enable Large Language Models (LLMs) to interact with tools. You will often see 'Function' and 'Tool' used interchangeably because 'functions' (blocks of reusable code) are the 'tools' agents use to carry out tasks. In order for a function's code to be invoked, an LLM must compare the users request against the functions description. To do this a schema containing the descriptions of all the available functions is sent to the LLM. The LLM then selects the most appropriate function for the task and returns its name and arguments. The selected function is invoked, it's response is sent back to the LLM, which uses the information to respond to the users request.

For developers to implement function calling for agents, you will need:

1. An LLM model that supports function calling
2. A schema containing function descriptions
3. The code for each function described

Let's use the example of getting the current time in a city to illustrate:

1. **Initialize an LLM that supports function calling:**

    Not all models support function calling, so it's important to check that the LLM you are using does.     <a href="https://learn.microsoft.com/azure/ai-services/openai/how-to/function-calling" target="_blank">Azure OpenAI</a> supports function calling. We can start by initiating the Azure OpenAI client. 

    ```python
    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
        api_version="2024-05-01-preview"
    )
    ```

1. **Create a Function Schema**:

    Next we will define a JSON schema that contains the function name, description of what the function does, and the names and descriptions of the function parameters.
    We will then take this schema and pass it to the client created previously, along with the users request to find the time in San Francisco. What's important to note is that a **tool call** is what is returned, **not** the final answer to the question. As mentioned earlier, the LLM returns the name of the function it selected for the task, and the arguments that will be passed to it.

    ```python
    # Function description for the model to read - RPS Tournament Tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "answer_tournament_question",
                "description": "Answer a RPS tournament question using knowledge base",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The tournament question to answer, e.g. 'What is the capital of France?'",
                        },
                        "difficulty": {
                            "type": "string", 
                            "description": "Question difficulty level: easy, medium, hard",
                            "enum": ["easy", "medium", "hard"]
                        }
                    },
                    "required": ["question"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "select_optimal_move",
                "description": "Select the optimal Rock, Paper, or Scissors move based on strategy analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "opponent_history": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Previous moves by opponents if available",
                        },
                        "round_number": {
                            "type": "integer",
                            "description": "Current round number in tournament"
                        },
                        "strategy": {
                            "type": "string",
                            "description": "Strategy to use: random, aggressive, defensive, counter",
                            "enum": ["random", "aggressive", "defensive", "counter"]
                        }
                    },
                    "required": ["round_number", "strategy"],
                },
            }
        }
    ]
    ```
   
    ```python
  
    # Initial user message - RPS tournament scenario
    messages = [{"role": "user", "content": "I need to answer this question for the RPS tournament: 'What is the capital of Japan?' and select my next move for round 3"}] 
  
    # First API call: Ask the model to use the function
      response = client.chat.completions.create(
          model=deployment_name,
          messages=messages,
          tools=tools,
          tool_choice="auto",
      )
  
      # Process the model's response
      response_message = response.choices[0].message
      messages.append(response_message)
  
      print("Model's response:")  

      print(response_message)
  
    ```

    ```bash
    Model's response:
    ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_pOsKdUlqvdyttYB67MOj434b', function=Function(arguments='{"question":"What is the capital of Japan?","difficulty":"easy"}', name='answer_tournament_question'), type='function'), ChatCompletionMessageToolCall(id='call_xYz123AbC789dEf456', function=Function(arguments='{"round_number":3,"strategy":"defensive"}', name='select_optimal_move'), type='function')])
    ```
  
1. **The function code required to carry out the task:**

    Now that the LLM has chosen which functions need to be run, the code that carries out the RPS tournament tasks needs to be implemented and executed.
    We can implement the code to answer tournament questions and select optimal moves. We will also need to write the code to extract the name and arguments from the response_message to get the final result.

    ```python
      def answer_tournament_question(question, difficulty="medium"):
        """Answer a RPS tournament question using knowledge base"""
        print(f"answer_tournament_question called with question: {question}, difficulty: {difficulty}")
        
        question_lower = question.lower()
        
        # Geography questions
        if "capital" in question_lower:
            if "japan" in question_lower:
                return json.dumps({"question": question, "answer": "Tokyo", "confidence": "high"})
            elif "france" in question_lower:
                return json.dumps({"question": question, "answer": "Paris", "confidence": "high"})
            elif "australia" in question_lower:
                return json.dumps({"question": question, "answer": "Canberra", "confidence": "high"})
        
        # Science questions  
        elif "largest ocean" in question_lower:
            return json.dumps({"question": question, "answer": "Pacific Ocean", "confidence": "high"})
        elif "fastest land animal" in question_lower:
            return json.dumps({"question": question, "answer": "Cheetah", "confidence": "high"})
        
        # Math questions
        elif any(op in question for op in ["+", "plus", "add"]):
            # Simple math parsing
            import re
            numbers = re.findall(r'\d+', question)
            if len(numbers) >= 2:
                result = sum(int(n) for n in numbers[:2])
                return json.dumps({"question": question, "answer": str(result), "confidence": "high"})
        
        # Default response
        return json.dumps({"question": question, "answer": "I need to research this question", "confidence": "low"})

      def select_optimal_move(round_number, strategy, opponent_history=None):
        """Select optimal Rock, Paper, or Scissors move based on strategy"""
        print(f"select_optimal_move called with round: {round_number}, strategy: {strategy}")
        
        moves = ["Rock", "Paper", "Scissors"]
        
        if strategy == "random":
            import random
            selected_move = random.choice(moves)
        elif strategy == "aggressive":
            # Aggressive strategy favors Rock (appears strong)
            selected_move = "Rock"
        elif strategy == "defensive":
            # Defensive strategy uses Paper (beats the common Rock)
            selected_move = "Paper"
        elif strategy == "counter":
            # Counter strategy based on opponent history
            if opponent_history and len(opponent_history) > 0:
                last_opponent_move = opponent_history[-1]
                if last_opponent_move == "Rock":
                    selected_move = "Paper"
                elif last_opponent_move == "Paper":
                    selected_move = "Scissors"
                elif last_opponent_move == "Scissors":
                    selected_move = "Rock"
                else:
                    selected_move = "Rock"  # Default
            else:
                selected_move = "Rock"  # Default when no history
        else:
            selected_move = "Rock"  # Safe default
            
        return json.dumps({
            "round_number": round_number,
            "selected_move": selected_move,
            "strategy_used": strategy,
            "reasoning": f"Selected {selected_move} using {strategy} strategy for round {round_number}"
        })
    ```

     ```python
     # Handle RPS tournament function calls
      if response_message.tool_calls:
          for tool_call in response_message.tool_calls:
              function_args = json.loads(tool_call.function.arguments)
              
              if tool_call.function.name == "answer_tournament_question":
                  question_response = answer_tournament_question(
                      question=function_args.get("question"),
                      difficulty=function_args.get("difficulty", "medium")
                  )
                  
                  messages.append({
                      "tool_call_id": tool_call.id,
                      "role": "tool",
                      "name": "answer_tournament_question",
                      "content": question_response,
                  })
                  
              elif tool_call.function.name == "select_optimal_move":
                  move_response = select_optimal_move(
                      round_number=function_args.get("round_number"),
                      strategy=function_args.get("strategy"),
                      opponent_history=function_args.get("opponent_history", [])
                  )
                  
                  messages.append({
                      "tool_call_id": tool_call.id,
                      "role": "tool", 
                      "name": "select_optimal_move",
                      "content": move_response,
                  })
      else:
          print("No tool calls were made by the model.")  
  
      # Second API call: Get the final response from the model
      final_response = client.chat.completions.create(
          model=deployment_name,
          messages=messages,
      )
  
      return final_response.choices[0].message.content
     ```

     ```bash
      answer_tournament_question called with question: What is the capital of Japan?, difficulty: easy
      select_optimal_move called with round: 3, strategy: defensive
      The capital of Japan is Tokyo. For round 3, I recommend using Paper as your move with a defensive strategy, which is effective against the commonly chosen Rock.
     ```

Function Calling is at the heart of most, if not all agent tool use design, however implementing it from scratch can sometimes be challenging.
As we learned in [Lesson 2](../02-explore-agentic-frameworks/) agentic frameworks provide us with pre-built building blocks to implement tool use.
 
## Tool Use Examples with Agentic Frameworks

Here are some examples of how you can implement the Tool Use Design Pattern using different agentic frameworks:

### Semantic Kernel

<a href="https://learn.microsoft.com/azure/ai-services/agents/overview" target="_blank">Semantic Kernel</a> is an open-source AI framework for .NET, Python, and Java developers working with Large Language Models (LLMs). It simplifies the process of using function calling by automatically describing your functions and their parameters to the model through a process called <a href="https://learn.microsoft.com/semantic-kernel/concepts/ai-services/chat-completion/function-calling/?pivots=programming-language-python#1-serializing-the-functions" target="_blank">serializing</a>. It also handles the back-and-forth communication between the model and your code. Another advantage of using an agentic framework like Semantic Kernel, is that it allows you to access pre-built tools like <a href="https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_agents/openai_assistant/step4_assistant_tool_file_search.py" target="_blank">File Search</a> and <a href="https://github.com/microsoft/semantic-kernel/blob/main/python/samples/getting_started_with_agents/openai_assistant/step3_assistant_tool_code_interpreter.py" target="_blank">Code Interpreter</a>.

The following diagram illustrates the process of function calling with Semantic Kernel:

![function calling](./images/functioncalling-diagram.png)

In Semantic Kernel functions/tools are called <a href="https://learn.microsoft.com/semantic-kernel/concepts/plugins/?pivots=programming-language-python" target="_blank">Plugins</a>. We can convert the RPS tournament functions we saw earlier into a plugin by turning them into a class with the functions in it. We can also import the `kernel_function` decorator, which takes in the description of the function. When you then create a kernel with the RPSTournamentPlugin, the kernel will automatically serialize the functions and their parameters, creating the schema to send to the LLM in the process.

```python
from semantic_kernel.functions import kernel_function

class RPSTournamentPlugin:
    """Plugin for RPS Tournament functionality"""

    @kernel_function(
        description="Answer a RPS tournament question using knowledge base"
    )
    def answer_tournament_question(self, question: str, difficulty: str = "medium") -> str:
        """Answer tournament questions with varying difficulty levels"""
        # Implementation here - same as the function we defined earlier
        question_lower = question.lower()
        
        if "capital" in question_lower and "japan" in question_lower:
            return "Tokyo"
        elif "largest ocean" in question_lower:
            return "Pacific Ocean"
        # ... other question handling logic
        
        return "I need to research this question"

    @kernel_function(
        description="Select optimal Rock, Paper, or Scissors move based on strategy analysis"
    )
    def select_optimal_move(self, round_number: int, strategy: str, opponent_history: list = None) -> str:
        """Select the best move for the current round"""
        moves = ["Rock", "Paper", "Scissors"]
        
        if strategy == "defensive":
            return "Paper"  # Beats the common Rock
        elif strategy == "aggressive":
            return "Rock"   # Appears strong
        elif strategy == "counter" and opponent_history:
            # Counter the last opponent move
            last_move = opponent_history[-1] if opponent_history else "Rock"
            if last_move == "Rock":
                return "Paper"
            elif last_move == "Paper":
                return "Scissors"
            else:
                return "Rock"
        else:
            import random
            return random.choice(moves)

```

```python 
from semantic_kernel import Kernel

# Create the kernel
kernel = Kernel()

# Create the plugin
psr_tournament_plugin = RPSTournamentPlugin()

# Add the plugin to the kernel
kernel.add_plugin(psr_tournament_plugin, plugin_name="psr_tournament")
```
  
### Azure AI Agent Service

<a href="https://learn.microsoft.com/azure/ai-services/agents/overview" target="_blank">Azure AI Agent Service</a> is a newer agentic framework that is designed to empower developers to securely build, deploy, and scale high-quality, and extensible AI agents without needing to manage the underlying compute and storage resources. It is particularly useful for enterprise applications since it is a fully managed service with enterprise grade security.

When compared to developing with the LLM API directly, Azure AI Agent Service provides some advantages, including:

- Automatic tool calling – no need to parse a tool call, invoke the tool, and handle the response; all of this is now done server-side
- Securely managed data – instead of managing your own conversation state, you can rely on threads to store all the information you need
- Out-of-the-box tools – Tools that you can use to interact with your data sources, such as Bing, Azure AI Search, and Azure Functions.

The tools available in Azure AI Agent Service can be divided into two categories:

1. Knowledge Tools:
    - <a href="https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/bing-grounding?tabs=python&pivots=overview" target="_blank">Grounding with Bing Search</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/file-search?tabs=python&pivots=overview" target="_blank">File Search</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/azure-ai-search?tabs=azurecli%2Cpython&pivots=overview-azure-ai-search" target="_blank">Azure AI Search</a>

2. Action Tools:
    - <a href="https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/function-calling?tabs=python&pivots=overview" target="_blank">Function Calling</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/code-interpreter?tabs=python&pivots=overview" target="_blank">Code Interpreter</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/openapi-spec?tabs=python&pivots=overview" target="_blank">OpenAI defined tools</a>
    - <a href="https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/azure-functions?pivots=overview" target="_blank">Azure Functions</a>

The Agent Service allows us to be able to use these tools together as a `toolset`. It also utilizes `threads` which keep track of the history of messages from a particular conversation.

Imagine you are a sales agent at a company called Contoso. You want to develop a conversational agent that can answer questions about your sales data.

The following image illustrates how you could use Azure AI Agent Service to analyze your sales data:

![Agentic Service In Action](./images/agent-service-in-action.jpg)

To use any of these tools with the service we can create a client and define a tool or toolset. To implement this practically we can use the following Python code. The LLM will be able to look at the toolset and decide whether to use the user created function, `fetch_sales_data_using_sqlite_query`, or the pre-built Code Interpreter depending on the user request.

```python 
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from fetch_sales_data_functions import fetch_sales_data_using_sqlite_query # fetch_sales_data_using_sqlite_query function which can be found in a fetch_sales_data_functions.py file.
from azure.ai.projects.models import ToolSet, FunctionTool, CodeInterpreterTool

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

# Initialize function calling agent with the fetch_sales_data_using_sqlite_query function and adding it to the toolset
fetch_data_function = FunctionTool(fetch_sales_data_using_sqlite_query)
toolset = ToolSet()
toolset.add(fetch_data_function)

# Initialize Code Interpreter tool and adding it to the toolset. 
code_interpreter = code_interpreter = CodeInterpreterTool()
toolset = ToolSet()
toolset.add(code_interpreter)

agent = project_client.agents.create_agent(
    model="gpt-4o-mini", name="my-agent", instructions="You are helpful agent", 
    toolset=toolset
)
```

## What are the special considerations for using the Tool Use Design Pattern to build trustworthy AI agents?

A common concern with SQL dynamically generated by LLMs is security, particularly the risk of SQL injection or malicious actions, such as dropping or tampering with the database. While these concerns are valid, they can be effectively mitigated by properly configuring database access permissions. For most databases this involves configuring the database as read-only. For database services like PostgreSQL or Azure SQL, the app should be assigned a read-only (SELECT) role.

Running the app in a secure environment further enhances protection. In enterprise scenarios, data is typically extracted and transformed from operational systems into a read-only database or data warehouse with a user-friendly schema. This approach ensures that the data is secure, optimized for performance and accessibility, and that the app has restricted, read-only access.
