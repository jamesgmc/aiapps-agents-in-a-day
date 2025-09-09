"""
PSR Game Agent V1 - Enhanced with Semantic Kernel Integration
This version demonstrates the concepts from lesson 52 (Explore Agentic Frameworks)
- Uses Semantic Kernel for AI-powered question answering
- Implements modular plugin architecture for extensibility
- Shows auto-function calling capabilities
"""

import random
import time
import threading
import asyncio
import os
from typing import Optional, List, Dict, Any

# Handle typing for older Python versions
try:
    from typing import Annotated
except ImportError:
    # For Python < 3.9
    try:
        from typing_extensions import Annotated
    except ImportError:
        # Fallback for when typing_extensions is not available
        def Annotated(type_hint, description):
            return type_hint

# Import Semantic Kernel components
try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureChatPromptExecutionSettings
    from semantic_kernel.connectors.ai import FunctionChoiceBehavior
    from semantic_kernel.contents import ChatHistory
    from semantic_kernel.functions import kernel_function
    SEMANTIC_KERNEL_AVAILABLE = True
except ImportError:
    SEMANTIC_KERNEL_AVAILABLE = False
    print("Semantic Kernel not available. Install with: pip install semantic-kernel")
    # Create dummy decorator for when SK is not available
    def kernel_function(name=None, description=None):
        def decorator(func):
            func._sk_function_name = name
            func._sk_description = description
            return func
        return decorator

from api_client import PSRGameClient


class PSRGamePluginV1:
    """PSR Game Plugin V1 - Semantic Kernel powered functions"""
    
    @kernel_function(name="answer_question", description="Answer tournament questions using AI knowledge")
    async def answer_question(
        self, question: Annotated[str, "The tournament question to answer"]
    ) -> str:
        """Enhanced question answering with better logic"""
        question_lower = question.lower()
        
        # Geography questions
        if "capital" in question_lower:
            if "france" in question_lower:
                return "Paris"
            elif "australia" in question_lower:
                return "Canberra"
            elif "japan" in question_lower:
                return "Tokyo"
            elif "germany" in question_lower:
                return "Berlin"
                
        # Science questions
        if "largest ocean" in question_lower:
            return "Pacific Ocean"
        elif "smallest planet" in question_lower:
            return "Mercury"
        elif "speed of light" in question_lower:
            return "299,792,458 meters per second"
            
        # Math questions
        if "+" in question or "plus" in question_lower:
            try:
                import re
                match = re.search(r'(\d+)\s*[\+\w]*\s*(\d+)', question)
                if match:
                    num1 = int(match.group(1))
                    num2 = int(match.group(2))
                    return str(num1 + num2)
            except:
                pass
                
        # Default intelligent response
        return f"Based on the question '{question}', I would need to research this topic further to provide an accurate answer."

    @kernel_function(name="select_strategic_move", description="Select optimal Rock, Paper, or Scissors move using strategy")
    async def select_strategic_move(
        self, strategy: Annotated[str, "Strategy hint like 'random', 'rock', 'counter_opponent', 'psychological'"]
    ) -> str:
        """Strategic move selection with multiple strategies"""
        moves = ["Rock", "Paper", "Scissors"]
        
        if strategy == "random":
            return random.choice(moves)
        elif strategy == "rock":
            return "Rock"
        elif strategy == "paper":
            return "Paper"
        elif strategy == "scissors":
            return "Scissors"
        elif strategy == "counter_rock":
            return "Paper"  # Paper beats Rock
        elif strategy == "counter_paper":
            return "Scissors"  # Scissors beats Paper
        elif strategy == "counter_scissors":
            return "Rock"  # Rock beats Scissors
        elif strategy == "psychological":
            # Use psychology - most beginners choose Rock first
            return "Paper"
        else:
            return "Rock"  # Safe default

    @kernel_function(name="analyze_tournament_status", description="Analyze current tournament situation and provide insights")
    async def analyze_tournament_status(
        self, current_round: Annotated[int, "Current round number"], 
        score: Annotated[int, "Current score"],
        total_rounds: Annotated[int, "Total rounds in tournament"] = 5
    ) -> str:
        """Analyze tournament progress and provide strategic insights"""
        rounds_remaining = total_rounds - current_round
        
        if current_round == 1:
            return "Tournament starting! Focus on accurate question answering and conservative move selection."
        elif rounds_remaining <= 2:
            return f"Critical phase! {rounds_remaining} rounds left. Current score: {score}. Time for strategic risk-taking."
        elif score > current_round * 2:  # Assuming max 2 points per round
            return f"Performing well! Score: {score}. Maintain current strategy."
        else:
            return f"Need improvement. Score: {score}. Consider adjusting strategy for remaining rounds."


class GameAgentV1:
    """
    PSR Game Agent V1 - Enhanced with Semantic Kernel Integration
    
    This version demonstrates lesson 52 concepts:
    - Modular components with Semantic Kernel
    - AI-powered function calling
    - Plugin architecture for extensibility
    """
    
    VERSION = "1.0.0"
    LESSON = "52 - Explore Agentic Frameworks"
    
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.client = PSRGameClient()
        self.player_id: Optional[int] = None
        self.current_round = 1
        self.tournament_status = "Not Started"
        self.round_status = "Not Started"
        self.is_running = False
        self.status_log: List[str] = []
        self.results: List[Dict] = []
        self.last_completed_round = 0
        self.latest_score = 0
        
        # Semantic Kernel setup
        self.kernel = None
        self.chat_service = None
        self.setup_semantic_kernel()
        
    def log_status(self, message: str):
        """Add a status message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [V{self.VERSION}] {message}"
        self.status_log.append(log_message)
        print(log_message)
    
    def setup_semantic_kernel(self):
        """Initialize Semantic Kernel components"""
        if not SEMANTIC_KERNEL_AVAILABLE:
            self.log_status("Semantic Kernel not available - falling back to basic mode")
            return
            
        try:
            # Create kernel
            self.kernel = Kernel()
            
            # Add plugin
            self.kernel.add_plugin(PSRGamePluginV1(), plugin_name="psr_game")
            
            # Note: In a real implementation, you would set up Azure OpenAI here
            # For demo purposes, we'll use the plugin functions directly
            self.log_status(f"Semantic Kernel initialized - Agent V{self.VERSION} ready!")
            
        except Exception as e:
            self.log_status(f"Semantic Kernel setup failed: {e}")
            
    async def answer_question_ai(self, question: str) -> str:
        """Use Semantic Kernel AI to answer questions"""
        if self.kernel and SEMANTIC_KERNEL_AVAILABLE:
            try:
                # Use the plugin directly for this demo
                plugin = PSRGamePluginV1()
                return await plugin.answer_question(question)
            except Exception as e:
                self.log_status(f"AI question answering failed: {e}")
                return self.answer_question_fallback(question)
        else:
            return self.answer_question_fallback(question)
    
    def answer_question_fallback(self, question: str) -> str:
        """Fallback question answering when Semantic Kernel is not available"""
        question_lower = question.lower()
        
        if "capital of france" in question_lower:
            return "Paris"
        elif "largest ocean" in question_lower:
            return "Pacific Ocean"
        elif "2 + 2" in question_lower:
            return "4"
        else:
            return "I need more information to answer this question accurately."
    
    async def select_move_ai(self, strategy: str = "random") -> int:
        """Use Semantic Kernel AI to select moves"""
        if self.kernel and SEMANTIC_KERNEL_AVAILABLE:
            try:
                plugin = PSRGamePluginV1()
                move_name = await plugin.select_strategic_move(strategy)
                return self.get_move_number(move_name)
            except Exception as e:
                self.log_status(f"AI move selection failed: {e}")
                return random.randint(0, 2)
        else:
            return random.randint(0, 2)
    
    def get_move_number(self, move_name: str) -> int:
        """Convert move name to number"""
        move_map = {"Rock": 0, "Paper": 1, "Scissors": 2}
        return move_map.get(move_name, 0)
    
    def get_move_name(self, move_number: Optional[int]) -> str:
        """Convert move number to name"""
        if move_number is None:
            return "None"
        move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
        return move_names.get(move_number, "Unknown")
    
    async def analyze_situation(self) -> str:
        """Analyze current tournament situation using AI"""
        if self.kernel and SEMANTIC_KERNEL_AVAILABLE:
            try:
                plugin = PSRGamePluginV1()
                return await plugin.analyze_tournament_status(
                    self.current_round, self.latest_score
                )
            except Exception as e:
                self.log_status(f"AI analysis failed: {e}")
                return "Tournament in progress - playing conservatively."
        else:
            return "Tournament in progress - playing conservatively."
    
    def register_player(self) -> bool:
        """Register the player with the server"""
        self.log_status(f"Registering player: {self.player_name} (Agent V{self.VERSION})")
        
        response = self.client.register_player(self.player_name)
        
        if "error" in response:
            self.log_status(f"Registration failed: {response['error']}")
            return False
        
        if "playerId" in response:
            self.player_id = response["playerId"]
            self.log_status(f"Registration successful! Player ID: {self.player_id}")
            return True
        else:
            self.log_status(f"Registration failed: {response.get('message', 'Unknown error')}")
            return False
    
    def start_autonomous_play(self):
        """Start autonomous play in a separate thread"""
        if self.is_running:
            self.log_status("Agent is already running!")
            return
            
        self.is_running = True
        self.log_status(f"Starting autonomous play with Agent V{self.VERSION} - {self.LESSON}")
        
        # Run in thread to avoid blocking
        def run_async():
            asyncio.run(self.monitor_and_play())
        
        thread = threading.Thread(target=run_async, daemon=True)
        thread.start()
    
    async def monitor_and_play(self):
        """Main game loop - monitors status and plays autonomously using AI"""
        while self.is_running:
            try:
                # Get current status
                status_response = self.client.get_player_status(self.player_id)
                
                if "error" in status_response:
                    self.log_status(f"Error getting status: {status_response['error']}")
                    time.sleep(2)
                    continue
                
                # Extract status information
                tournament_status = status_response.get("tournamentStatus")
                round_status = status_response.get("roundStatus")
                current_round = status_response.get("currentRound", 1)
                question = status_response.get("question")
                can_submit = status_response.get("canSubmit", False)
                
                # Update internal state
                self.current_round = current_round
                
                # Handle different states
                if tournament_status == 2:  # Completed
                    self.log_status("Tournament completed!")
                    await self.get_final_results()
                    break
                
                if tournament_status == 1 and round_status == 1 and can_submit and question:
                    # Round is in progress and we can submit
                    self.log_status(f"Processing Round {current_round} question with AI...")
                    
                    # Get strategic analysis
                    analysis = await self.analyze_situation()
                    self.log_status(f"Strategic analysis: {analysis}")
                    
                    # Answer the question using AI
                    answer = await self.answer_question_ai(question)
                    self.log_status(f"AI generated answer: {answer}")
                    
                    # Choose RPS move using AI strategy
                    strategy = "psychological" if current_round <= 2 else "random"
                    rps_move = await self.select_move_ai(strategy)
                    move_name = self.get_move_name(rps_move)
                    self.log_status(f"AI selected move ({strategy} strategy): {move_name}")
                    
                    # Submit answer and move
                    submit_response = self.client.submit_answer(
                        self.player_id, current_round, answer, rps_move
                    )
                    
                    if "error" in submit_response:
                        self.log_status(f"Submission failed: {submit_response['error']}")
                    else:
                        self.log_status(f"Submitted successfully for Round {current_round}")
                
                # Get current results
                await self.get_current_results()
                
                # Wait before next check
                time.sleep(2)
                
            except Exception as e:
                self.log_status(f"Error in game loop: {e}")
                time.sleep(2)
    
    async def get_current_results(self):
        """Get current results and update results list"""
        if not self.player_id:
            return
        
        results_response = self.client.get_player_results(self.player_id)
        
        if "error" in results_response:
            self.log_status(f"Error getting current results: {results_response['error']}")
            return
        
        self.results = results_response if isinstance(results_response, list) else []
        
        if self.results:
            latest_result = self.results[-1]
            round_num = latest_result.get("roundNumber", "?")
            score = latest_result.get("score", 0)
            self.latest_score = score
            
            if round_num > self.last_completed_round:
                self.last_completed_round = round_num
                self.log_status(f"Round {round_num} completed! Current score: {score}")
    
    async def get_final_results(self):
        """Get and display final tournament results"""
        await self.get_current_results()
        
        if self.results:
            total_score = sum(result.get("score", 0) for result in self.results)
            self.log_status(f"Final Results - Total Score: {total_score}")
            self.log_status(f"Agent V{self.VERSION} tournament performance complete!")
        else:
            self.log_status("No results available")
        
        self.is_running = False


# Usage example for standalone testing
if __name__ == "__main__":
    async def test_agent():
        agent = GameAgentV1("AI_Agent_V1")
        
        # Test AI components
        print(f"Testing Agent V{agent.VERSION} - {agent.LESSON}")
        
        # Test question answering
        test_questions = [
            "What is the capital of France?",
            "What is 5 + 3?",
            "What is the largest ocean?"
        ]
        
        for question in test_questions:
            answer = await agent.answer_question_ai(question)
            print(f"Q: {question}")
            print(f"A: {answer}\n")
        
        # Test move selection
        strategies = ["random", "psychological", "counter_rock"]
        for strategy in strategies:
            move = await agent.select_move_ai(strategy)
            move_name = agent.get_move_name(move)
            print(f"Strategy: {strategy} -> Move: {move_name}")
        
        # Test analysis
        analysis = await agent.analyze_situation()
        print(f"\nTournament Analysis: {analysis}")
    
    # Run tests
    asyncio.run(test_agent())