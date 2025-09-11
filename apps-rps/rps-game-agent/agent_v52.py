import random
import re
import os
import json
import requests
from typing import Optional

# Try to import dotenv, but don't fail if not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If dotenv is not available, just continue without it
    pass


class GameAgentV52:
    """Azure AI Agent service-based agent class for handling questions and move decisions in RPS Tournament using Azure AI Foundry Agent"""
    
    def __init__(self, azure_ai_endpoint: Optional[str] = None, azure_ai_key: Optional[str] = None, agent_id: Optional[str] = None):
        """
        Initialize the Azure AI Agent service-based game agent using Azure AI Foundry Agent
        
        Args:
            azure_ai_endpoint: Azure AI Foundry endpoint URL
            azure_ai_key: Azure AI service API key
            agent_id: Azure AI Foundry Agent ID (created in portal)
        """
        self.azure_ai_endpoint = azure_ai_endpoint or os.getenv('AZURE_AI_ENDPOINT')
        self.azure_ai_key = azure_ai_key or os.getenv('AZURE_AI_KEY')
        self.agent_id = agent_id or os.getenv('AZURE_AI_AGENT_ID')

        # Initialize headers for Azure AI API calls
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.azure_ai_key}' if self.azure_ai_key else None
        }
        
        # Agent instructions for RPS tournament (similar to FlightAgent but for game context)
        self.agent_instructions = """
        You are RPSAgent, a virtual assistant specialized in handling Paper-Scissors-Rock tournament queries and decisions. Your role includes answering knowledge questions accurately and making strategic game moves. Follow the instructions below to ensure clarity and effectiveness in your responses:

        ### Task Instructions:
        1. **Answering Questions**:
           - For math problems, provide only the numerical answer
           - For knowledge questions, provide brief, factual answers
           - Keep responses short and direct (under 50 characters)
           - Be accurate and concise

        2. **Making Game Moves**:
           - For Rock-Paper-Scissors decisions, choose strategically
           - Consider tournament context and winning patterns
           - Respond with only: Rock, Paper, or Scissors
           
        3. **Response Format**:
           - Use a tone that is clear, concise, and competitive
           - Provide direct answers without unnecessary elaboration
           - Focus on accuracy and strategic thinking
        """
    
    def _call_azure_ai_agent(self, prompt: str, conversation_id: Optional[str] = None) -> str:
        """
        Call Azure AI Agent service using the agent created in Azure AI Foundry portal
        
        Args:
            prompt: The user prompt/question
            conversation_id: Optional conversation ID for context
            
        Returns:
            Response from Azure AI agent
        """
        try:
            # If agent_id is available, use the agents API endpoint
            if self.agent_id:
                # Use Azure AI Foundry Agent API endpoint
                endpoint_url = f"{self.azure_ai_endpoint}/agents/{self.agent_id}/chat"
                
                payload = {
                    "message": prompt,
                    "conversation_id": conversation_id,
                    "instructions": self.agent_instructions,
                    "max_tokens": 150,
                    "temperature": 0.1
                }
            else:
                # Fallback to regular chat completions with agent-like instructions
                endpoint_url = f"{self.azure_ai_endpoint}/chat/completions"
                
                payload = {
                    "messages": [
                        {
                            "role": "system",
                            "content": self.agent_instructions
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
            
            # Make API call to Azure AI Agent service
            response = requests.post(
                endpoint_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Handle different response formats from agent vs chat completions
                if self.agent_id:
                    # Agent API response format
                    return result.get('message', {}).get('content', '').strip()
                else:
                    # Chat completions response format
                    return result.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
            else:
                print(f"Azure AI Agent API error: {response.status_code} - {response.text}")
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
        # Create a specific prompt for question answering
        prompt = f"Please answer this question accurately and concisely: {question}"
        
        # Try Azure AI Agent service first
        azure_answer = self._call_azure_ai_agent(prompt)
        
        if azure_answer:
            # Clean up the response to extract just the answer
            cleaned_answer = azure_answer.strip()
            
            # Remove common prefixes and keep it concise
            if cleaned_answer.lower().startswith(('the answer is', 'answer:', 'result:')):
                cleaned_answer = cleaned_answer.split(':', 1)[-1].strip()
            
            # For mathematical expressions, try to extract just the number
            if any(op in question for op in ['+', '-', '*', '/', '=']):
                number_match = re.search(r'\b\d+(?:\.\d+)?\b', cleaned_answer)
                if number_match:
                    return number_match.group()
            
            return cleaned_answer[:50]  # Limit response length
        
        # Fallback to simple local processing if Azure AI fails
        return self._local_fallback_answer(question)
    
    def _local_fallback_answer(self, question: str) -> str:
        """
        Local fallback for basic question answering when Azure AI is unavailable
        
        Args:
            question: The question to answer
            
        Returns:
            Basic answer or "Unknown"
        """
        question_lower = question.lower()
        
        # Simple math operations
        if '+' in question:
            try:
                # Extract numbers around the + sign
                import re
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = sum(int(num) for num in numbers)
                    return str(result)
            except:
                pass
        
        if '-' in question:
            try:
                # Extract numbers around the - sign
                import re
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = int(numbers[0]) - int(numbers[1])
                    return str(result)
            except:
                pass
        
        # Basic knowledge
        if 'capital' in question_lower and 'france' in question_lower:
            return "Paris"
        elif 'color' in question_lower and 'sky' in question_lower:
            return "Blue"
        
        return "Unknown"
    
    def choose_rps_move(self) -> int:
        """
        Choose Rock (0), Paper (1), or Scissors (2) using Azure AI Agent service or random selection
        
        Returns:
            Move selection as integer (0=Rock, 1=Paper, 2=Scissors)
        """
        # Create a specific prompt for RPS move selection
        prompt = """In a Rock-Paper-Scissors tournament game, choose the best strategic move. 
        This is part of a competitive tournament and you want to win.
        Respond with only one word: Rock, Paper, or Scissors."""
        
        azure_choice = self._call_azure_ai_agent(prompt)
        
        if azure_choice:
            choice_lower = azure_choice.lower().strip()
            if 'rock' in choice_lower:
                return 0
            elif 'paper' in choice_lower:
                return 1
            elif 'scissors' in choice_lower or 'scissor' in choice_lower:
                return 2
        
        # Fallback to random choice if Azure AI fails
        return random.randint(0, 2)


# Backward compatibility - maintain same interface as original GameAgent
class GameAgent(GameAgentV52):
    """Alias for backward compatibility with existing code"""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Initialize agent
    agent = GameAgentV52()
    
    # Test question answering
    test_questions = [
        "What is 15 + 27?",
        "What is the capital of France?",
        "What color is the sky?",
        "What is 100 - 35?"
    ]
    
    print("Testing Azure AI Agent V52 (Azure AI Foundry Agent):")
    print("=" * 50)
    
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print()
    
    # Test RPS move selection
    print("RPS Move Selection Test:")
    move_names = ["Rock", "Paper", "Scissors"]
    for i in range(5):
        move = agent.choose_rps_move()
        print(f"Move {i+1}: {move_names[move]} ({move})")
    
    print("\nAgent V52 testing complete!")