"""
RPS Game Agent V2 - Enhanced with Advanced Tool Use
This version demonstrates the concepts from lesson 54 (Tool Use Design Pattern)
- Implements comprehensive tool/function calling capabilities
- Multiple specialized tools for different RPS tournament tasks
- Error handling and validation for tool usage
- State management across tool interactions
"""

import random
import time
import threading
import asyncio
import json
import os
from typing import Optional, List, Dict, Any

# Handle typing for older Python versions
try:
    from typing import Annotated
except ImportError:
    try:
        from typing_extensions import Annotated
    except ImportError:
        def Annotated(type_hint, description):
            return type_hint

# Import Semantic Kernel components if available
try:
    from semantic_kernel import Kernel
    from semantic_kernel.functions import kernel_function
    SEMANTIC_KERNEL_AVAILABLE = True
except ImportError:
    SEMANTIC_KERNEL_AVAILABLE = False
    print("Semantic Kernel not available. Install with: pip install semantic-kernel")
    def kernel_function(name=None, description=None):
        def decorator(func):
            func._sk_function_name = name
            func._sk_description = description
            return func
        return decorator

from api_client import RPSGameClient


class RPSTournamentToolsV2:
    """Comprehensive tool collection for RPS tournament functionality"""
    
    @kernel_function(name="answer_question", description="Answer tournament questions using comprehensive knowledge base")
    async def answer_tournament_question(
        self, 
        question: Annotated[str, "The tournament question to answer"],
        difficulty: Annotated[str, "Question difficulty: easy, medium, hard"] = "medium"
    ) -> str:
        """Enhanced question answering with comprehensive knowledge base"""
        question_lower = question.lower()
        
        # Geography questions
        if "capital" in question_lower:
            capitals = {
                "france": "Paris",
                "japan": "Tokyo", 
                "australia": "Canberra",
                "germany": "Berlin",
                "italy": "Rome",
                "spain": "Madrid",
                "canada": "Ottawa",
                "brazil": "Brasília",
                "china": "Beijing",
                "india": "New Delhi",
                "russia": "Moscow",
                "egypt": "Cairo"
            }
            for country, capital in capitals.items():
                if country in question_lower:
                    return json.dumps({
                        "answer": capital,
                        "confidence": "high",
                        "category": "geography",
                        "difficulty_assessed": difficulty
                    })
        
        # Science questions
        science_answers = {
            "largest ocean": "Pacific Ocean",
            "smallest planet": "Mercury", 
            "fastest land animal": "Cheetah",
            "tallest mountain": "Mount Everest",
            "longest river": "Nile River",
            "largest mammal": "Blue Whale",
            "speed of light": "299,792,458 meters per second",
            "chemical formula for water": "H2O",
            "number of bones in human body": "206"
        }
        
        for key, answer in science_answers.items():
            if key in question_lower:
                return json.dumps({
                    "answer": answer,
                    "confidence": "high", 
                    "category": "science",
                    "difficulty_assessed": difficulty
                })
        
        # Math questions
        if any(op in question for op in ["+", "plus", "add"]):
            try:
                import re
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = sum(int(n) for n in numbers)
                    return json.dumps({
                        "answer": str(result),
                        "confidence": "high",
                        "category": "mathematics",
                        "calculation": f"{' + '.join(numbers)} = {result}"
                    })
            except:
                pass
        
        if any(op in question for op in ["-", "minus", "subtract"]):
            try:
                import re
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = int(numbers[0]) - int(numbers[1])
                    return json.dumps({
                        "answer": str(result),
                        "confidence": "high",
                        "category": "mathematics",
                        "calculation": f"{numbers[0]} - {numbers[1]} = {result}"
                    })
            except:
                pass
                
        # History questions
        history_answers = {
            "first president": "George Washington",
            "world war 2 ended": "1945",
            "moon landing": "1969",
            "berlin wall fell": "1989"
        }
        
        for key, answer in history_answers.items():
            if key in question_lower:
                return json.dumps({
                    "answer": answer,
                    "confidence": "medium",
                    "category": "history"
                })
        
        # Default intelligent response
        return json.dumps({
            "answer": "I need to research this topic further",
            "confidence": "low",
            "category": "unknown",
            "research_required": True
        })

    @kernel_function(name="analyze_move", description="Analyze and select optimal RPS move using advanced strategy")
    async def analyze_optimal_move(
        self,
        round_number: Annotated[int, "Current round number"],
        strategy: Annotated[str, "Strategy: random, aggressive, defensive, counter, psychological"],
        opponent_history: Annotated[List[str], "Previous opponent moves"] = None,
        game_score: Annotated[int, "Current game score"] = 0
    ) -> str:
        """Advanced move selection with multiple strategies and analysis"""
        
        moves = ["Rock", "Paper", "Scissors"]
        reasoning = []
        
        if strategy == "random":
            selected_move = random.choice(moves)
            reasoning.append("Using random strategy for unpredictability")
            
        elif strategy == "aggressive":
            # Rock appears strong and aggressive
            selected_move = "Rock"
            reasoning.append("Rock conveys strength and aggression")
            
        elif strategy == "defensive":
            # Paper beats the most common move (Rock)
            selected_move = "Paper" 
            reasoning.append("Paper beats Rock, the most commonly chosen move")
            
        elif strategy == "counter":
            if opponent_history and len(opponent_history) > 0:
                last_move = opponent_history[-1]
                if last_move == "Rock":
                    selected_move = "Paper"
                    reasoning.append(f"Countering opponent's last move: {last_move} with Paper")
                elif last_move == "Paper":
                    selected_move = "Scissors" 
                    reasoning.append(f"Countering opponent's last move: {last_move} with Scissors")
                elif last_move == "Scissors":
                    selected_move = "Rock"
                    reasoning.append(f"Countering opponent's last move: {last_move} with Rock")
                else:
                    selected_move = "Rock"
                    reasoning.append("Unknown opponent move, defaulting to Rock")
            else:
                selected_move = "Rock"
                reasoning.append("No opponent history available, choosing safe Rock")
                
        elif strategy == "psychological":
            if round_number == 1:
                # Most beginners choose Rock first
                selected_move = "Paper"
                reasoning.append("First round: most players choose Rock, selecting Paper")
            elif round_number <= 3:
                # Early rounds, people avoid obvious patterns
                selected_move = random.choice(["Paper", "Scissors"])
                reasoning.append("Early round: avoiding Rock, alternating between Paper/Scissors")
            else:
                # Later rounds, people get more random
                selected_move = random.choice(moves)
                reasoning.append("Late round: players become more unpredictable")
                
        else:
            # Adaptive strategy based on score
            if game_score < 0:
                selected_move = "Paper"  # Safe choice
                reasoning.append("Behind in score, playing conservatively with Paper")
            elif game_score > 3:
                selected_move = "Rock"  # Aggressive when winning
                reasoning.append("Ahead in score, playing aggressively with Rock")
            else:
                selected_move = random.choice(moves)
                reasoning.append("Even score, playing unpredictably")
        
        return json.dumps({
            "selected_move": selected_move,
            "round_number": round_number,
            "strategy_used": strategy,
            "reasoning": reasoning,
            "confidence": "high" if strategy in ["counter", "psychological"] else "medium",
            "opponent_analysis": {
                "history_length": len(opponent_history) if opponent_history else 0,
                "last_move": opponent_history[-1] if opponent_history else None
            }
        })

    @kernel_function(name="validate_submission", description="Validate tournament submission before sending")
    async def validate_tournament_submission(
        self,
        question: Annotated[str, "Tournament question"],
        answer: Annotated[str, "Proposed answer"], 
        move: Annotated[str, "Selected RPS move"],
        round_number: Annotated[int, "Current round number"]
    ) -> str:
        """Validate submission data before sending to tournament server"""
        
        validation_results = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        # Validate move
        valid_moves = ["Rock", "Paper", "Scissors"]
        if move not in valid_moves:
            validation_results["is_valid"] = False
            validation_results["errors"].append(f"Invalid move: {move}. Must be one of {valid_moves}")
        
        # Validate answer
        if not answer or len(answer.strip()) == 0:
            validation_results["is_valid"] = False
            validation_results["errors"].append("Answer cannot be empty")
        elif len(answer) > 500:
            validation_results["warnings"].append("Answer is very long, consider shortening")
        
        # Validate round number
        if round_number < 1 or round_number > 5:
            validation_results["warnings"].append(f"Unusual round number: {round_number}")
        
        # Check answer quality
        if answer.lower() in ["i don't know", "unknown", "not sure"]:
            validation_results["suggestions"].append("Consider providing a more confident answer")
        
        # Check for obvious answer patterns
        if len(answer) == 1:
            validation_results["warnings"].append("Very short answer - make sure it's complete")
        
        return json.dumps(validation_results)

    @kernel_function(name="analyze_performance", description="Analyze tournament performance and suggest improvements")
    async def analyze_tournament_performance(
        self,
        results: Annotated[List[Dict], "Tournament results so far"],
        current_round: Annotated[int, "Current round number"]
    ) -> str:
        """Analyze performance and provide strategic recommendations"""
        
        if not results:
            return json.dumps({
                "total_rounds": 0,
                "average_score": 0,
                "recommendations": ["Start playing to gather performance data"]
            })
        
        total_score = sum(r.get("score", 0) for r in results)
        correct_answers = sum(1 for r in results if r.get("answerCorrect", False))
        total_rounds = len(results)
        
        analysis = {
            "total_rounds": total_rounds,
            "total_score": total_score,
            "average_score": total_score / total_rounds if total_rounds > 0 else 0,
            "correct_answers": correct_answers,
            "answer_accuracy": correct_answers / total_rounds if total_rounds > 0 else 0,
            "recommendations": []
        }
        
        # Performance recommendations
        if analysis["answer_accuracy"] < 0.5:
            analysis["recommendations"].append("Focus on improving question answering accuracy")
        
        if analysis["average_score"] < 1.0:
            analysis["recommendations"].append("Consider more strategic move selection")
        
        if total_rounds >= 3:
            recent_scores = [r.get("score", 0) for r in results[-3:]]
            if all(s < 1 for s in recent_scores):
                analysis["recommendations"].append("Recent performance decline - adjust strategy")
        
        # Strategic insights
        moves_used = [r.get("move") for r in results if r.get("move") is not None]
        if moves_used:
            move_counts = {move: moves_used.count(move) for move in [0, 1, 2]}  # Rock, Paper, Scissors
            most_used = max(move_counts, key=move_counts.get)
            if move_counts[most_used] > len(moves_used) * 0.6:
                move_names = {0: "Rock", 1: "Paper", 2: "Scissors"}
                analysis["recommendations"].append(f"You're using {move_names[most_used]} too often - vary your moves")
        
        return json.dumps(analysis)


class GameAgentV2:
    """
    RPS Game Agent V2 - Enhanced with Advanced Tool Use
    
    This version demonstrates lesson 54 concepts:
    - Tool Use Design Pattern implementation
    - Multiple specialized tools for different tasks
    - Function/tool calling with comprehensive error handling
    - State management across tool interactions
    """
    
    VERSION = "2.0.0"
    LESSON = "54 - Tool Use Design Pattern"
    
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.client = RPSGameClient()
        self.player_id: Optional[int] = None
        self.current_round = 1
        self.tournament_status = "Not Started"
        self.round_status = "Not Started"
        self.is_running = False
        self.status_log: List[str] = []
        self.results: List[Dict] = []
        self.last_completed_round = 0
        self.latest_score = 0
        
        # Tool system setup
        self.tools = RPSTournamentToolsV2()
        self.setup_tool_system()
        
    def log_status(self, message: str):
        """Add a status message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [V{self.VERSION}] {message}"
        self.status_log.append(log_message)
        print(log_message)
    
    def setup_tool_system(self):
        """Initialize the tool system"""
        self.log_status(f"Tool system initialized - Agent V{self.VERSION} ready!")
        self.log_status("Available tools: question answering, move analysis, validation, performance analysis")
    
    async def use_tool_answer_question(self, question: str, difficulty: str = "medium") -> Dict:
        """Use the question answering tool"""
        try:
            result = await self.tools.answer_tournament_question(question, difficulty)
            return json.loads(result)
        except Exception as e:
            self.log_status(f"Tool error (answer_question): {e}")
            return {"answer": "Unable to answer", "confidence": "low", "error": str(e)}
    
    async def use_tool_analyze_move(self, round_number: int, strategy: str, opponent_history: List[str] = None, score: int = 0) -> Dict:
        """Use the move analysis tool"""
        try:
            result = await self.tools.analyze_optimal_move(round_number, strategy, opponent_history, score)
            return json.loads(result)
        except Exception as e:
            self.log_status(f"Tool error (analyze_move): {e}")
            return {"selected_move": "Rock", "reasoning": ["Error in analysis"], "error": str(e)}
    
    async def use_tool_validate_submission(self, question: str, answer: str, move: str, round_number: int) -> Dict:
        """Use the validation tool"""
        try:
            result = await self.tools.validate_tournament_submission(question, answer, move, round_number)
            return json.loads(result)
        except Exception as e:
            self.log_status(f"Tool error (validate_submission): {e}")
            return {"is_valid": True, "warnings": [], "errors": [str(e)]}
    
    async def use_tool_analyze_performance(self) -> Dict:
        """Use the performance analysis tool"""
        try:
            result = await self.tools.analyze_tournament_performance(self.results, self.current_round)
            return json.loads(result)
        except Exception as e:
            self.log_status(f"Tool error (analyze_performance): {e}")
            return {"recommendations": ["Error in performance analysis"], "error": str(e)}
    
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
        """Main game loop - monitors status and plays using advanced tools"""
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
                    self.log_status(f"Processing Round {current_round} question using advanced tools...")
                    
                    # Tool 1: Answer the question
                    answer_result = await self.use_tool_answer_question(question, "medium")
                    answer = answer_result.get("answer", "Unknown")
                    self.log_status(f"Tool result - Answer: {answer} (confidence: {answer_result.get('confidence', 'unknown')})")
                    
                    # Tool 2: Analyze optimal move
                    strategy = "psychological" if current_round <= 2 else "counter" if current_round <= 4 else "random"
                    move_result = await self.use_tool_analyze_move(current_round, strategy, [], self.latest_score)
                    selected_move = move_result.get("selected_move", "Rock")
                    reasoning = move_result.get("reasoning", [])
                    self.log_status(f"Tool result - Move: {selected_move} (strategy: {strategy})")
                    self.log_status(f"Move reasoning: {', '.join(reasoning)}")
                    
                    # Tool 3: Validate submission
                    validation_result = await self.use_tool_validate_submission(question, answer, selected_move, current_round)
                    if not validation_result.get("is_valid", True):
                        self.log_status(f"Validation errors: {validation_result.get('errors', [])}")
                        # Fix issues if possible
                        if "Invalid move" in str(validation_result.get("errors", [])):
                            selected_move = "Rock"  # Safe fallback
                            self.log_status("Fixed move to Rock due to validation error")
                    
                    warnings = validation_result.get("warnings", [])
                    if warnings:
                        self.log_status(f"Validation warnings: {warnings}")
                    
                    # Submit answer and move
                    rps_move_number = self.get_move_number(selected_move)
                    submit_response = self.client.submit_answer(
                        self.player_id, current_round, answer, rps_move_number
                    )
                    
                    if "error" in submit_response:
                        self.log_status(f"Submission failed: {submit_response['error']}")
                    else:
                        self.log_status(f"Submitted successfully for Round {current_round}")
                
                # Get current results and analyze performance
                await self.get_current_results()
                
                # Tool 4: Analyze performance (every few rounds)
                if current_round > 1 and current_round % 2 == 0:
                    performance_result = await self.use_tool_analyze_performance()
                    recommendations = performance_result.get("recommendations", [])
                    if recommendations:
                        self.log_status(f"Performance recommendations: {', '.join(recommendations)}")
                
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
            # Use performance analysis tool for final summary
            final_analysis = await self.use_tool_analyze_performance()
            total_score = final_analysis.get("total_score", 0)
            accuracy = final_analysis.get("answer_accuracy", 0)
            
            self.log_status(f"Final Results - Total Score: {total_score}, Answer Accuracy: {accuracy:.1%}")
            self.log_status(f"Agent V{self.VERSION} with advanced tools tournament complete!")
            
            recommendations = final_analysis.get("recommendations", [])
            if recommendations:
                self.log_status(f"Final recommendations: {', '.join(recommendations)}")
        else:
            self.log_status("No results available")
        
        self.is_running = False


# Usage example for standalone testing
if __name__ == "__main__":
    async def test_agent_tools():
        agent = GameAgentV2("AI_Agent_V2_Tools")
        
        print(f"Testing Agent V{agent.VERSION} - {agent.LESSON}")
        
        # Test question answering tool
        test_questions = [
            ("What is the capital of Japan?", "easy"),
            ("What is the largest ocean?", "medium"), 
            ("What is 15 + 27?", "easy"),
            ("Who was the first president?", "hard")
        ]
        
        for question, difficulty in test_questions:
            result = await agent.use_tool_answer_question(question, difficulty)
            print(f"Q: {question}")
            print(f"A: {result.get('answer')} (confidence: {result.get('confidence')})")
            print(f"Category: {result.get('category', 'unknown')}\n")
        
        # Test move analysis tool  
        strategies = ["random", "psychological", "counter", "aggressive", "defensive"]
        for strategy in strategies:
            result = await agent.use_tool_analyze_move(3, strategy, ["Rock", "Paper"], 2)
            print(f"Strategy: {strategy} -> Move: {result.get('selected_move')}")
            print(f"Reasoning: {', '.join(result.get('reasoning', []))}\n")
        
        # Test validation tool
        validation = await agent.use_tool_validate_submission(
            "What is 2+2?", "4", "Rock", 1
        )
        print(f"Validation: {validation}")
        
        # Test performance analysis (with mock data)
        agent.results = [
            {"roundNumber": 1, "score": 2, "answerCorrect": True, "move": 0},
            {"roundNumber": 2, "score": 1, "answerCorrect": False, "move": 1},
            {"roundNumber": 3, "score": 2, "answerCorrect": True, "move": 0}
        ]
        performance = await agent.use_tool_analyze_performance()
        print(f"Performance Analysis: {performance}")
    
    # Run tests
    asyncio.run(test_agent_tools())