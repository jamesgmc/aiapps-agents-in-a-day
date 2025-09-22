import re
import os
import requests
from dotenv import load_dotenv
# https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/function-calling?pivots=python
# https://code.visualstudio.com/mcp
# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_telemetry/sample_agents_basics_async_with_azure_monitor_tracing.py
# https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/model-context-protocol-samples?pivots=python
load_dotenv()


class GameAgent:
    """Simple AI agent for Rock-Paper-Scissors tournament"""
    
    def __init__(self, azure_ai_endpoint=None, azure_ai_key=None):
        # Get Azure AI credentials from environment or parameters
        self.endpoint = azure_ai_endpoint or os.getenv('AZURE_OPENAI_API_ENDPOINT')
        self.key = azure_ai_key or os.getenv('AZURE_OPENAI_API_KEY')
        
        # Setup HTTP headers for API calls
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.key}'
        }
    
    def _ask_ai(self, question, system_prompt=None):
        """Send question to Azure AI and get response"""
        if not system_prompt:
            system_prompt = "You are a helpful assistant. Answer questions clearly and briefly."
        
        # Prepare the API request
        data = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 150,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"AI API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error calling AI: {e}")
            return None
    
    def answer_question(self, question):
        """Answer tournament questions using AI"""
        system_prompt = """You are participating in a Rock-Paper-Scissors tournament. 
        Answer questions clearly and briefly. For math problems, give just the number."""
        
        print(f"Question: {question}")
        answer = self._ask_ai(question, system_prompt)
        print(f"Answer: {answer}")
        
        if not answer:
            return "Unknown"
        
        # Clean up the answer
        answer = answer.strip()
        
        # Remove common prefixes
        prefixes = ['the answer is', 'answer:', 'result:']
        for prefix in prefixes:
            if answer.lower().startswith(prefix):
                answer = answer.split(':', 1)[-1].strip()
        
        # For math questions, extract just the number
        if any(symbol in question for symbol in ['+', '-', '*', '/', '=']):
            numbers = re.findall(r'\d+(?:\.\d+)?', answer)
            if numbers:
                return numbers[0]
        
        # Limit answer length
        return answer[:50]


if __name__ == "__main__":

    print("Game Agent: Test starting...")
    # Test questions
    test_questions = [
        "What is the capital of France?", 
    ]
    
    with GameAgent() as agent:
        for question in test_questions:
            answer = agent.answer_question(question)
            print(f"Q: {question}")
            print(f"A: {answer}")
            print()
    
    print("Game Agent: Test complete")