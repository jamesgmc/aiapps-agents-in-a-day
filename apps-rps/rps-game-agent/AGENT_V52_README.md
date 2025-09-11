# Agent V52 - Azure AI Agent Service Integration

## Overview

`agent_v52.py` implements a PSR (Paper-Scissors-Rock) tournament game agent using Azure AI Agent service, following the concepts from the "52-create-first-agent" documentation.

## Key Features

### Azure AI Agent Service Integration
- Uses Azure AI Foundry Agent API endpoints when configured with an agent ID
- Falls back to regular chat completions API for backward compatibility
- Specialized agent instructions tailored for PSR tournament context

### Agent Instructions
The agent is configured with specialized instructions for:
- **Question Answering**: Accurate and concise responses for math and knowledge questions
- **Strategic Game Play**: Smart Rock-Paper-Scissors move selection for tournament play
- **Tournament Context**: Understanding of competitive PSR tournament environment

### Robust Fallback System
- **Azure AI Service**: Primary method using configured Azure endpoints
- **Local Processing**: Fallback for basic math and knowledge questions
- **Error Handling**: Graceful degradation when services are unavailable

## Configuration

### Environment Variables
Add to your `.env` file:

```bash
# Azure AI Foundry Configuration
AZURE_AI_ENDPOINT=https://your-azure-ai-endpoint.cognitiveservices.azure.com
AZURE_AI_KEY=your-azure-ai-api-key-here

# Azure AI Foundry Agent ID (for agent_v52.py)
# Create an agent in Azure AI Foundry portal and use its ID here
AZURE_AI_AGENT_ID=your-azure-agent-id-here
```

### Azure AI Foundry Agent Setup
1. Create an agent in Azure AI Foundry portal
2. Use PSR-specific instructions (similar to FlightAgent example)
3. Deploy and obtain the agent ID
4. Configure the agent ID in your environment

## Usage

### Basic Usage
```python
from agent_v52 import GameAgentV52

# Initialize the agent
agent = GameAgentV52()

# Answer questions
answer = agent.answer_question("What is 15 + 27?")
print(f"Answer: {answer}")

# Make RPS moves
move = agent.choose_rps_move()  # Returns 0 (Rock), 1 (Paper), or 2 (Scissors)
```

### Drop-in Replacement
```python
# Replace this:
from agent_v1 import GameAgent

# With this:
from agent_v52 import GameAgent

# Everything else works the same!
```

### Integration with GameProcessor
The agent maintains full compatibility with the existing `GameProcessor` class:

```python
# In game_processor.py, you can change:
from agent_v1 import GameAgent

# To:
from agent_v52 import GameAgent

# No other changes needed!
```

## API Compatibility

The agent maintains 100% API compatibility with `agent_v1.py`:

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `answer_question(question: str)` | `question`: Question string | `str`: Answer | Answers tournament questions |
| `choose_rps_move()` | None | `int`: 0-2 | Chooses Rock (0), Paper (1), or Scissors (2) |

## Testing

Run the included tests to verify functionality:

```bash
# Test interface compatibility
python test_agent_v52.py

# Test as drop-in replacement (requires dependencies)
python test_drop_in_replacement.py

# Run the agent directly
python agent_v52.py
```

## Differences from agent_v1.py

| Feature | agent_v1.py | agent_v52.py |
|---------|-------------|--------------|
| API Endpoint | Chat Completions | Azure AI Agent Service |
| Agent Configuration | System messages | Azure AI Foundry Agent |
| Instructions | Basic prompts | Specialized PSR tournament agent |
| Fallback | Random/simple | Enhanced local processing |
| Configuration | Basic endpoint/key | Agent ID + endpoint/key |

## Error Handling

The agent includes comprehensive error handling:
- **Network Issues**: Graceful fallback to local processing
- **Authentication**: Clear error messages for missing credentials
- **API Errors**: Detailed logging of service responses
- **Validation**: Input validation and response processing

## Benefits of Azure AI Agent Service

1. **Specialized Agents**: Purpose-built agents with specific instructions
2. **Improved Context**: Better understanding of tournament environment
3. **Enhanced Performance**: Optimized for specific use cases
4. **Scalability**: Leverages Azure AI infrastructure
5. **Management**: Easy configuration through Azure AI Foundry portal