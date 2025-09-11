import re
import os
import json
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class GameAgentV1:
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        self.azure_ai_endpoint = azure_ai_endpoint or os.getenv('AZURE_AI_ENDPOINT')
        self.azure_ai_key = azure_ai_key or os.getenv('AZURE_AI_KEY')

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.azure_ai_key}' if self.azure_ai_key else None
        }
    
    def _call_azure_ai_agent(self, prompt: str, system_message: str = None) -> str:
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": system_message or "You are a helpful assistant specialized in answering questions accurately and concisely."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 150,
            "temperature": 0.1,
            "top_p": 0.9
        }
        
        response = requests.post(
            f"{self.azure_ai_endpoint}",
            headers=self.headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        else:
            print(f"Azure AI API error: {response.status_code} - {response.text}")
            return None
                
    
    def answer_question(self, question: str) -> str:
        system_message = """
        You are a knowledgeable assistant participating in a Paper-Scissors-Rock tournament. 
        You need to answer questions accurately and concisely. 
        For math problems, provide only the numerical answer. 
        For knowledge questions, provide brief, factual answers.
        Keep responses short and direct.
        """
        
        print("answer_question=" + question)
        azure_answer = self._call_azure_ai_agent(question, system_message)
        print("answer_question=" + azure_answer)
        
        if azure_answer:
            cleaned_answer = azure_answer.strip()
            if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
            
            if any(op in question for op in ['+', '-', '*', '/', '=']):
                number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                if number_match:
                    return number_match.group()
            
            return cleaned_answer[:50]
        
    
    def choose_rps_move(self) -> int:
        prompt = """
        In a Rock-Paper-Scissors game, choose the best move. 
        Respond with only one word: Rock, Paper, or Scissors.
        Consider that this is part of a tournament and you want to win."""
        
        system_message = "You are a strategic Rock-Paper-Scissors player. Choose wisely."
        print("choose_rps_move=" + system_message)
        azure_choice = self._call_azure_ai_agent(prompt, system_message)
        print("choose_rps_move=" + azure_choice)
        if azure_choice:
            choice_lower = azure_choice.lower().strip()
            if 'rock' in choice_lower:
                return 0
            elif 'paper' in choice_lower:
                return 1
            elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                return 2
        
    


class GameAgent(GameAgentV1):
    """Backward compatibility alias"""
    pass
if __name__ == "__main__":
    agent = GameAgentV1()
    
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?",
        "What color is the sky?",
        "What is 100 - 35?"
    ]
    
    print("Testing Azure AI Agent V1:")
    print("=" * 40)
    
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    
    print("RPS Move Selection Test:")
    for i in range(5):
        move = agent.choose_rps_move()
