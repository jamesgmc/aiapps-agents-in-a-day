import os
from dotenv import load_dotenv
import autogen
from autogen import ConversableAgent
import openai

load_dotenv()


class GameAgent:
    """AutoGen Agent service for RPS Tournament"""
    
    def __init__(self, project_endpoint=None, model_deployment_name=None, player_name=None):
        self.player_name = player_name or os.getenv('DEV_Name', 'default-player')
        self.agent_name = f"rps-game-agent-{self.player_name}"
        
        # Configure LLM for AutoGen
        self.llm_config = {
            "config_list": [
                {
                    "model": os.getenv('AZURE_OPENAI_API_DEPLOYMENT_NAME'),
                    "api_key": os.getenv('AZURE_OPENAI_API_KEY'),
                    "base_url": os.getenv('AZURE_OPENAI_API_ENDPOINT'),
                    "api_type": "azure",
                    "api_version": "2024-02-15-preview"
                }
            ],
            "temperature": 0.7,
        }
        
        # Also setup direct OpenAI client as fallback
        self.openai_client = openai.AzureOpenAI(
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv('AZURE_OPENAI_API_ENDPOINT')
        )
        
        self.agent = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def _setup_agent(self):
        """Setup the AutoGen agent"""
        if not self.agent:
            try:
                self.agent = ConversableAgent(
                    name=self.agent_name,
                    system_message=f"You are {self.player_name}, a helpful assistant that can answer questions and play Rock-Paper-Scissors games. Be concise and direct in your responses. Always provide a clear, single answer.",
                    llm_config=self.llm_config,
                    human_input_mode="NEVER",
                    max_consecutive_auto_reply=5,
                )
                print(f"Created AutoGen agent: {self.agent_name}")
            except Exception as e:
                print(f"Failed to create AutoGen agent: {e}")
                self.agent = None
        
    def _call_autogen_agent(self, message):
        """Call AutoGen agent or fallback to direct OpenAI"""
        if not self.agent:
            self._setup_agent()
        
        # If AutoGen agent is available, try to use it
        messages = [{"role": "user", "content": message}]
        response = self.agent.generate_reply(messages=messages)
        
        if isinstance(response, str) and response.strip() and "TERMINATING" not in response:
            return response
        elif isinstance(response, dict) and 'content' in response:
            return response['content']

        return None
        
    
    def answer_question(self, question):
        """Generate an answer to the question using AutoGen agent"""
        if not self.agent:
            self._setup_agent()
        return self._call_autogen_agent(question)
        
    def choose_rps_move(self):
        """Choose Rock (0), Paper (1), or Scissors (2) using AutoGen agent"""
        prompt = "You are playing Rock-Paper-Scissors. Choose the best strategic move. Respond with only one word: Rock, Paper, or Scissors."
        
        if not self.agent:
            self._setup_agent()
        autogen_choice = self._call_autogen_agent(prompt)
        choice_lower = autogen_choice.lower().strip()
        
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