import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FunctionTool, FileSearchTool, FilePurpose
from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from azure.ai.agents.models import (
    ListSortOrder,
    McpTool,
    RequiredMcpToolCall,
    RunStepActivityDetails,
    SubmitToolApprovalAction,
    ToolApproval,
)
import time

load_dotenv()


class GameAgent:
    """Azure AI Foundry Agent service for RPS Tournament with Human-in-the-Loop"""
    
    def __init__(self, project_endpoint=None, model_deployment_name=None, player_name=None):
        self.project_endpoint = project_endpoint or os.getenv('AZURE_FOUNDRY_PROJECT_ENDPOINT')
        self.model_deployment_name = model_deployment_name or os.getenv('AZURE_FOUNDRY_MODEL_DEPLOYMENT_NAME')
        self.player_name = player_name or os.getenv('DEV_Name', 'default-player')
        
        self.project_client = AIProjectClient(
            endpoint=self.project_endpoint,
            credential=DefaultAzureCredential()
        )
        
        self.agent_name = f"rps-game-agent-human-loop-{self.player_name}"
        self.agent = None
        self.thread = None
        self._client_context = None
    
    def __enter__(self):
        self._client_context = self.project_client.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._client_context:
            return self.project_client.__exit__(exc_type, exc_val, exc_tb)
    
    def _find_existing_agent(self):
        """Find existing agent by name"""
        agents = self.project_client.agents.list_agents()
        for agent in agents:
            if agent.name == self.agent_name:
                return agent
        return None
    
    def _setup_agent(self):
        """Setup the Azure AI agent - reuse existing or create new"""
        existing_agent = self._find_existing_agent()
        
        if existing_agent:
            self.project_client.agents.delete_agent(existing_agent.id)
            print(f"Deleted existing agent: {self.agent_name}")
        
        tools = self._setup_tools()
        self.agent = self.project_client.agents.create_agent(
            model=self.model_deployment_name,
            name=self.agent_name,
            instructions=f"You are {self.player_name}, a helpful assistant that can answer questions and play Rock-Paper-Scissors games. When you need to use tools, ask for human approval first.",
            tools=tools
        )
        print(f"Created new agent: {self.agent_name}")
        
        self.thread = self.project_client.agents.threads.create()
    
    def _request_human_approval(self, tool_call):
        """Request human approval for tool execution"""
        print("\n" + "="*60)
        print("🤖 AGENT REQUESTING TOOL APPROVAL")
        print("="*60)
        print(f"Tool Name: {tool_call.function.name}")
        print(f"Tool Arguments: {tool_call.function.arguments}")
        print(f"Tool Call ID: {tool_call.id}")
        print("-"*60)
        
        # Parse and display arguments in a readable format
        try:
            import json
            args = json.loads(tool_call.function.arguments)
            print("Tool will be called with:")
            for key, value in args.items():
                print(f"  {key}: {value}")
        except:
            print(f"Raw arguments: {tool_call.function.arguments}")
        
        print("-"*60)
        
        # Ask for human approval
        while True:
            response = input("Do you want to approve this tool call? (y/yes/n/no): ").lower().strip()
            if response in ['y', 'yes']:
                print("✅ Tool call APPROVED by human")
                return True
            elif response in ['n', 'no']:
                print("❌ Tool call REJECTED by human")
                return False
            else:
                print("Please enter 'y/yes' to approve or 'n/no' to reject.")
    
    def _call_azure_ai_agent(self, message):
        """Call Azure AI Foundry Agent service with human-in-the-loop approval"""
        self.project_client.agents.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )
        
        run = self.project_client.agents.runs.create(
            thread_id=self.thread.id,
            agent_id=self.agent.id
        )
        print(f"Created run, ID: {run.id}")
        
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = self.project_client.agents.runs.get(thread_id=self.thread.id, run_id=run.id)
            print(f"Run status: {run.status}")
            
            if run.status == "requires_action":
                # Check if this is a tool approval request (human-in-the-loop)
                if hasattr(run.required_action, 'submit_tool_approval'):
                    print("🔄 Processing tool approval request...")
                    tool_calls = run.required_action.submit_tool_approval.tool_calls
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
                    print("📝 Tool approvals submitted")
                
                # Handle regular tool output requests
                elif hasattr(run.required_action, 'submit_tool_outputs'):
                    print("🔄 Processing tool output request...")
                    tool_calls = run.required_action.submit_tool_outputs.tool_calls
                    tool_outputs = []
                    
                    for tool_call in tool_calls:
                        if tool_call.function.name == "math_tool_function":
                            import json
                            args = json.loads(tool_call.function.arguments)
                            output = GameAgent.math_tool_function(args.get("expression", ""))
                            tool_outputs.append({"tool_call_id": tool_call.id, "output": output})
                            print(f"✅ Executed tool: {tool_call.function.name}")
                    
                    self.project_client.agents.runs.submit_tool_outputs(
                        thread_id=self.thread.id, 
                        run_id=run.id, 
                        tool_outputs=tool_outputs
                    )
                    print("📝 Tool outputs submitted")
        
        print(f"Run completed with status: {run.status}")
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
            
        # Get the latest messages
        messages = self.project_client.agents.messages.list(thread_id=self.thread.id)
        
        for message in messages:
            if message.role == "assistant":
                return message.content[0].text.value
        
        return "No response"
    
    def answer_question(self, question):
        """Generate an answer to the question using Azure AI Foundry Agent service"""
        if not self.agent:
            self._setup_agent()
        return self._call_azure_ai_agent(question)
        
    def choose_rps_move(self):
        """Choose Rock (0), Paper (1), or Scissors (2) using Azure AI Foundry Agent service"""
        prompt = "You are playing Rock-Paper-Scissors. Choose the best strategic move. Respond with only one word: Rock, Paper, or Scissors."
        
        if not self.agent:
            self._setup_agent()
        azure_choice = self._call_azure_ai_agent(prompt)
        choice_lower = azure_choice.lower().strip()
        
        if 'rock' in choice_lower:
            return 0
        elif 'paper' in choice_lower:
            return 1
        elif 'scissors' in choice_lower:
            return 2
        
        return 0
    
    @staticmethod
    def math_tool_function(expression: str) -> str:
        """
        Calculate mathematical expressions.

        :param expression: The mathematical expression to calculate.
        :return: Result of the calculation as a string.
        """
        try:
            print(f'🧮 Executing math calculation: {expression}')
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {str(e)}"
        
    def _setup_tools(self):
        """Setup tool functions for the agent"""
        user_functions = {GameAgent.math_tool_function}
        functions = FunctionTool(functions=user_functions)
        return functions.definitions



if __name__ == "__main__":

    print("Game Agent: Test starting...")
    test_questions = [
        "What is 15 + 27?"
    ]
    
    with GameAgent() as agent:
        for question in test_questions:
            answer = agent.answer_question(question)
            print(f"Q: {question}")
            print(f"A: {answer}")
            print()
    
    print("Game Agent: Test complete")

