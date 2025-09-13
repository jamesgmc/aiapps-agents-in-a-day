import os
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.planning.basic_planner import BasicPlanner

class GameAgentSK:
    """Semantic Kernel Agent for RPS Tournament"""

    def __init__(self, model_deployment_name=None, player_name=None, api_key=None):
        self.model_deployment_name = model_deployment_name or os.getenv('MODEL_DEPLOYMENT_NAME', 'gpt-3.5-turbo')
        self.player_name = player_name or os.getenv('PLAYER_NAME', 'default-player')
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.kernel = Kernel()
        self.kernel.add_chat_service(
            "chat_completion",
            OpenAIChatCompletion(self.model_deployment_name, self.api_key)
        )
        self.planner = BasicPlanner(self.kernel)

    def answer_question(self, question):
        prompt = f"You are {self.player_name}, a helpful assistant. Answer the following question:\n{question}"
        result = self.kernel.chat_service.complete(prompt)
        return result

    def choose_rps_move(self):
        prompt = (
            "You are playing Rock-Paper-Scissors. "
            "Choose the best strategic move. Respond with only one word: Rock, Paper, or Scissors."
        )
        result = self.kernel.chat_service.complete(prompt)
        choice_lower = result.lower().strip()
        if 'rock' in choice_lower:
            return 0
        elif 'paper' in choice_lower:
            return 1
        elif 'scissors' in choice_lower:
            return 2
        return 0

if __name__ == "__main__":
    test_questions = [
        "What is 15 + 27?"
    ]
    print("Testing Semantic Kernel Agent:")
    print("=" * 50)
    agent = GameAgentSK()
    print(f"Player Name: {agent.player_name}")
    print()
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    print("RPS Move Selection Test:")
    move_names = ["Rock", "Paper", "Scissors"]
    move = agent.choose_rps_move()
    print(f"Move: {move_names[move]} ({move})")
    print("\nAgent SK testing complete!")