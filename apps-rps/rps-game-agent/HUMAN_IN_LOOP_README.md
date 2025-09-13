# Human-in-the-Loop AI Agent

This implementation demonstrates how to add human approval workflows to Azure AI Agents, allowing humans to approve or reject tool executions before they occur.

## 🎯 Overview

Human-in-the-loop (HITL) is a design pattern that keeps humans involved in AI decision-making processes. This implementation shows how to:

- Request human approval before executing tools
- Provide clear information about what tools will do
- Allow humans to approve or reject tool executions
- Maintain full transparency in AI operations

## 🚀 Quick Start

### Basic Usage

```python
from agent_v67 import GameAgentV67

# Create agent with human-in-the-loop capabilities
with GameAgentV67() as agent:
    # This will request approval before using math tools
    answer = agent.answer_question("What is 15 + 27?")
    print(f"Answer: {answer}")
```

### Run the Example

```bash
# Run the interactive demonstration
python human_in_loop_example.py

# Or run the agent directly
python agent_v67.py
```

## 🏗️ Architecture

### Core Components

1. **Tool Approval Request**: Agent identifies need for tool use and requests approval
2. **Human Interface**: Console prompts for approval decisions  
3. **Approval Processing**: Submit approvals back to the agent
4. **Conditional Execution**: Tools only execute if approved

### Key Framework Methods

```python
# Check for tool approval requests
if hasattr(run.required_action, 'submit_tool_approval'):
    tool_calls = run.required_action.submit_tool_approval.tool_calls
    
    # Request human approval for each tool call
    tool_approvals = []
    for tool_call in tool_calls:
        approved = self._request_human_approval(tool_call)
        tool_approvals.append(
            ToolApproval(tool_call_id=tool_call.id, approved=approved)
        )
    
    # Submit approvals
    self.project_client.agents.runs.submit_tool_approvals(
        thread_id=self.thread.id,
        run_id=run.id,
        tool_approvals=tool_approvals
    )
```

## 💡 Features

### Interactive Approval Process

When the agent wants to use a tool, it will display:

```
🤖 AGENT REQUESTING TOOL APPROVAL
============================================================
Tool Name: math_tool_function  
Tool Arguments: {"expression": "15 + 27"}
Tool Call ID: call_abc123
------------------------------------------------------------
Tool will be called with:
  expression: 15 + 27
------------------------------------------------------------
Do you want to approve this tool call? (y/yes/n/no): 
```

### Human Control

- **Approve**: Type `y` or `yes` to allow tool execution
- **Reject**: Type `n` or `no` to prevent tool execution
- **Clear Information**: See exactly what the tool will do
- **Full Control**: Nothing happens without your approval

## 🔧 Implementation Details

### Agent Setup

```python
class GameAgentV67:
    def _setup_agent(self):
        # Agent configured to request approval
        self.agent = self.project_client.agents.create_agent(
            model=self.model_deployment_name,
            name=self.agent_name,
            instructions="When you need to use tools, ask for human approval first.",
            tools=tools
        )
```

### Approval Logic

```python
def _request_human_approval(self, tool_call):
    """Request human approval for tool execution"""
    # Display tool information
    print(f"Tool Name: {tool_call.function.name}")
    print(f"Tool Arguments: {tool_call.function.arguments}")
    
    # Get human decision
    while True:
        response = input("Approve this tool call? (y/yes/n/no): ").lower().strip()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y/yes' to approve or 'n/no' to reject.")
```

## 📋 Use Cases

### When to Use Human-in-the-Loop

1. **High-Stakes Operations**: When tool executions have significant consequences
2. **Learning Phase**: When training or validating agent behavior
3. **Compliance**: When regulations require human oversight
4. **Trust Building**: When users need confidence in AI decisions
5. **Error Prevention**: When preventing unwanted actions is critical

### Example Scenarios

- **Financial Operations**: Approve transactions before execution
- **System Administration**: Review commands before running
- **Data Processing**: Confirm data modifications
- **External API Calls**: Validate API requests
- **File Operations**: Approve file changes

## 🎛️ Configuration Options

### Environment Variables

```bash
PROJECT_ENDPOINT=your_azure_ai_project_endpoint
MODEL_DEPLOYMENT_NAME=your_model_deployment
PLAYER_NAME=your_player_name
```

### Customization

You can customize the approval interface by modifying:

- `_request_human_approval()`: Change the approval UI
- Agent instructions: Modify when approval is requested
- Tool setup: Control which tools require approval

## 🔍 Examples

### Math Calculations
```python
# Agent will request approval before calculating
agent.answer_question("What is 100 * 25?")
```

### Rock-Paper-Scissors
```python
# Agent will use approved tools for strategic decisions
move = agent.choose_rps_move()
```

### Custom Questions
```python
# Any question that triggers tool use will request approval
agent.answer_question("Calculate the square root of 144")
```

## 🛡️ Safety & Security

### Benefits

- **Transparency**: See exactly what tools will do
- **Control**: Nothing executes without permission
- **Auditability**: Track all approval decisions
- **Flexibility**: Approve some tools, reject others

### Best Practices

1. **Clear Tool Descriptions**: Make tool purposes obvious
2. **Detailed Arguments**: Show what data tools will process
3. **Consistent UI**: Use standardized approval interfaces
4. **Logging**: Record approval decisions for audit
5. **Timeout Handling**: Handle cases where humans don't respond

## 🚀 Advanced Usage

### Custom Approval Logic

```python
def _request_human_approval(self, tool_call):
    # Add custom logic here
    if tool_call.function.name == "critical_operation":
        # Require additional confirmation for critical ops
        return self._request_critical_approval(tool_call)
    else:
        # Standard approval process
        return self._standard_approval(tool_call)
```

### Integration with UI

The approval mechanism can be extended to work with:
- Web interfaces
- Mobile applications  
- Slack/Teams integrations
- Custom approval workflows

## 📚 References

- [Azure AI Agents Documentation](https://docs.microsoft.com/azure/ai)
- [Tool Use Design Patterns](../../../docs/50-AI-Agents/5-tool-use/)
- [Trustworthy AI Practices](../../../docs/50-AI-Agents/8-trustworthy-safety/)

## 🤝 Contributing

To extend this implementation:

1. Fork the repository
2. Add new approval mechanisms
3. Enhance the user interface
4. Add more tool types
5. Submit a pull request

---

**Note**: This implementation is designed for demonstration and learning purposes. For production use, consider additional security measures, logging, and error handling.