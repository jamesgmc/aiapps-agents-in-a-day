import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

# Load environment variables
load_dotenv()

class GameAgent:
    """Semantic Kernel Agent for RPS Tournament"""

    def __init__(self, model_deployment_name=None, player_name=None, api_key=None, endpoint=None, api_version=None):
        self.model_deployment_name = model_deployment_name or os.getenv('AZURE_OPENAI_API_DEPLOYMENT_NAME') or os.getenv('AZURE_FOUNDRY_MODEL_DEPLOYMENT_NAME', 'gpt-4o')
        self.player_name = player_name or os.getenv('DEV_Name', 'default-player')
        self.api_key = api_key or os.getenv('AZURE_OPENAI_API_KEY')
        self.endpoint = endpoint or os.getenv('AZURE_OPENAI_API_ENDPOINT')
        self.api_version = api_version or os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        self.kernel = Kernel()
        
        # Add Azure chat completion service to kernel
        chat_service = AzureChatCompletion(
            service_id="chat_completion",
            deployment_name=self.model_deployment_name,
            endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version
        )
        self.kernel.add_service(chat_service)

    def answer_question(self, question):
        prompt = f"You are {self.player_name}, a helpful assistant. Answer the following question:\n{question}"
        result = asyncio.run(self.kernel.invoke_prompt(prompt))
        return str(result)

    def choose_rps_move(self):
        prompt = (
            "You are playing Rock-Paper-Scissors. "
            "Choose the best strategic move. Respond with only one word: Rock, Paper, or Scissors."
        )
        result = asyncio.run(self.kernel.invoke_prompt(prompt))
        choice_lower = str(result).lower().strip()
        if 'rock' in choice_lower:
            return 0
        elif 'paper' in choice_lower:
            return 1
        elif 'scissors' in choice_lower:
            return 2
        return 0

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