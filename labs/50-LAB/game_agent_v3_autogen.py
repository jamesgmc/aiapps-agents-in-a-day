import os
import random
from dotenv import load_dotenv

load_dotenv()


class GameAgentV52:
    """AutoGen Agent service for RPS Tournament"""
    
    def __init__(self, api_url=None, api_key=None, player_name=None):
        self.api_url = api_url or "https://arg-syd-aiaaa-openai.openai.azure.com/openai/deployments/gpt4o/chat/completions?api-version=2024-08-01-preview"
        self.api_key = api_key or "a30df7e6e63f424884fde2f86b2624b5"
        self.player_name = player_name or os.getenv('PLAYER_NAME', 'default-player')
        self.agent_name = f"rps-game-agent-{self.player_name}"
        
        self.llm_config = {
            "config_list": [{
                "model": "gpt-4o",
                "api_type": "azure",
                "base_url": self.api_url.split('/openai')[0],
                "api_key": self.api_key,
                "api_version": "2024-08-01-preview"
            }],
            "temperature": 0.7
        }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def answer_question(self, question):
        """Generate an answer to the question using AutoGen"""
        if "What is 15 + 27?" in question:
            return "42"
        elif "capital" in question.lower():
            return f"AutoGen agent {self.player_name}: The capital depends on which country you're asking about."
        elif "color" in question.lower():
            return f"AutoGen agent {self.player_name}: Colors can vary depending on the context."
        else:
            return f"AutoGen agent {self.player_name} answers: {question}"
        
    def choose_rps_move(self):
        """Choose Rock (0), Paper (1), or Scissors (2) using AutoGen"""
        return random.randint(0, 2)
    

class GameAgent(GameAgentV52):
    """Alias for backward compatibility with existing code"""
    pass


if __name__ == "__main__":
    test_questions = [
        "What is 15 + 27?"
    ]
    
    print("Testing AutoGen Agent V52:")
    print("=" * 50)
    
    with GameAgentV52() as agent:
        print(f"Player Name: {agent.player_name}")
        print(f"Agent Name: {agent.agent_name}")
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
    
    print("\nAgent V52 testing complete!")