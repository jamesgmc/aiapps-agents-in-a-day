import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()


class GameAgentV52:
    """Azure AI Foundry Agent service for RPS Tournament"""
    
    def __init__(self, project_endpoint=None, model_deployment_name=None):
        self.project_endpoint = project_endpoint or os.getenv('PROJECT_ENDPOINT')
        self.model_deployment_name = model_deployment_name or os.getenv('MODEL_DEPLOYMENT_NAME')
        
        self.project_client = AIProjectClient(
            endpoint=self.project_endpoint,
            credential=DefaultAzureCredential()
        )
        
        self.agent = None
        self.thread = None
    
    def _setup_agent(self):
        """Setup the Azure AI agent"""
        self.agent = self.project_client.agents.create_agent(
            model=self.model_deployment_name,
            name="rps-game-agent",
            instructions="You are a helpful assistant that can answer questions and play Rock-Paper-Scissors games."
        )
        
        self.thread = self.project_client.agents.threads.create()
    
    def _call_azure_ai_agent(self, message):
        """Call Azure AI Foundry Agent service"""
        self.project_client.agents.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )
        
        run = self.project_client.agents.runs.create_and_process(
            thread_id=self.thread.id,
            agent_id=self.agent.id
        )
        
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
# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV52):
    """Alias for backward compatibility with existing code"""
    pass


if __name__ == "__main__":
    agent = GameAgentV52()
    
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?",
        "What color is the sky?",
        "What is 100 - 35?"
    ]
    
    print("Testing Azure AI Foundry Agent V52:")
    print("=" * 50)
    
    with agent.project_client:
        for question in test_questions:
            answer = agent.answer_question(question)
            print(f"Q: {question}")
            print(f"A: {answer}")
            print()
        
        print("RPS Move Selection Test:")
        move_names = ["Rock", "Paper", "Scissors"]
        for i in range(5):
            move = agent.choose_rps_move()
            print(f"Move {i+1}: {move_names[move]} ({move})")
    
    print("\nAgent V52 testing complete!")