import os
import requests
import json
from dotenv import load_dotenv
import autogen

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
        
        self.assistant = autogen.AssistantAgent(
            name=self.agent_name,
            system_message=f"You are {self.player_name}, a helpful assistant that can answer questions and play Rock-Paper-Scissors games.",
            llm_config=self.llm_config
        )
        
        self.user_proxy = autogen.UserProxyAgent(
            name="user",
            human_input_mode="NEVER",
            code_execution_config=False
        )
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def _call_autogen_agent(self, message):
        """Call AutoGen agent"""
        self.user_proxy.initiate_chat(
            self.assistant,
            message=message,
            silent=True
        )
        
        chat_history = self.user_proxy.chat_messages[self.assistant]
        if chat_history:
            return chat_history[-1]['content']
        
        return "No response"
    
    def answer_question(self, question):
        """Generate an answer to the question using AutoGen"""
        return self._call_autogen_agent(question)
        
    def choose_rps_move(self):
        """Choose Rock (0), Paper (1), or Scissors (2) using AutoGen"""
        prompt = "You are playing Rock-Paper-Scissors. Choose the best strategic move. Respond with only one word: Rock, Paper, or Scissors."
        
        autogen_choice = self._call_autogen_agent(prompt)
        choice_lower = autogen_choice.lower().strip()
        
        if 'rock' in choice_lower:
            return 0
        elif 'paper' in choice_lower:
            return 1
        elif 'scissors' in choice_lower:
            return 2
        
        return 0
    

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