import random
import re
import os
import json
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GameAgentV1:
    """Azure AI Agent service-based agent class for handling questions and move decisions in PSR Tournament"""
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None):
        """
        Initialize the Azure AI Agent service-based game agent
        
        Args:
            azure_ai_endpoint: Azure AI Foundry endpoint URL
            azure_ai_key: Azure AI service API key
        """
        self.azure_ai_endpoint = azure_ai_endpoint or os.getenv('AZURE_AI_ENDPOINT')
        self.azure_ai_key = azure_ai_key or os.getenv('AZURE_AI_KEY')

        # Initialize headers for Azure AI API calls
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.azure_ai_key}' if self.azure_ai_key else None
        }
    
    def _call_azure_ai_agent(self, prompt: str, system_message: str = None) -> str:
        """
        Call Azure AI Agent service with the given prompt
        
        Args:
            prompt: The user prompt/question
            system_message: Optional system message for context
            
        Returns:
            Response from Azure AI agent
        """
        try:
            # Construct the payload for Azure AI Agent service
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
                "temperature": 0.1,  # Low temperature for consistent answers
                "top_p": 0.9
            }
            
            # Make API call to Azure AI Agent service
            response = requests.post(
                f"{self.azure_ai_endpoint}/chat/completions",
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
                
        except Exception as e:
            print(f"Error calling Azure AI Agent service: {str(e)}")
            return None
    
    def answer_question(self, question: str) -> str:
        """
        Generate an answer to the question using Azure AI Agent service or local fallback
        
        Args:
            question: The question to answer
            
        Returns:
            Answer to the question
        """
        # Try Azure AI Agent service first
        system_message = """You are a knowledgeable assistant participating in a Paper-Scissors-Rock tournament. 
        You need to answer questions accurately and concisely. 
        For math problems, provide only the numerical answer. 
        For knowledge questions, provide brief, factual answers.
        Keep responses short and direct."""
        
        azure_answer = self._call_azure_ai_agent(question, system_message)
        
        if azure_answer:
            # Clean up the response to extract just the answer
            # Remove common prefixes and keep it concise
            cleaned_answer = azure_answer.strip()
            if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
            
            # For mathematical expressions, try to extract just the number
            if any(op in question for op in ['+', '-', '*', '/', '=']):
                number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                if number_match:
                    return number_match.group()
            
            return cleaned_answer[:50]  # Limit response length
        
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using Azure AI Agent service or random selection
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        # Use Azure AI to make a strategic move choice
        prompt = """In a Rock-Paper-Scissors game, choose the best move. 
        Respond with only one word: Rock, Paper, or Scissors.
        Consider that this is part of a tournament and you want to win."""
        
        system_message = "You are a strategic Rock-Paper-Scissors player. Choose wisely."
        
        azure_choice = self._call_azure_ai_agent(prompt, system_message)
        
        if azure_choice:
            choice_lower = azure_choice.lower().strip()
            if 'rock' in choice_lower:
                return 0
            elif 'paper' in choice_lower:
                return 1
            elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                return 2
        
    


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV1):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize agent
    agent = GameAgentV1()
    
    # Test question answering
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
    
    # Test RPS move selection
    print("RPS Move Selection Test:")
    for i in range(5):
        move = agent.choose_rps_move()
