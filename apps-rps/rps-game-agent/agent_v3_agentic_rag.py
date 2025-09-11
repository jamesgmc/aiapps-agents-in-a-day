"""
RPS Game Agent V3 - Enhanced with Agentic RAG
This version demonstrates the concepts from lesson 55 (Agentic RAG)
- Implements iterative retrieval-augmented generation
- Autonomous query refinement and source selection
- Self-correction mechanisms and confidence evaluation
- Memory and state management across retrieval iterations
"""

import random
import time
import threading
import asyncio
import json
import os
from typing import Optional, List, Dict, Any, Tuple

# Handle typing for older Python versions
try:
    from typing import Annotated
except ImportError:
    try:
        from typing_extensions import Annotated
    except ImportError:
        def Annotated(type_hint, description):
            return type_hint

from api_client import RPSGameClient


class RPSKnowledgeBase:
    """Simulated knowledge base for RPS tournament questions"""
    
    def __init__(self):
        # Simulated vector database with knowledge entries
        self.knowledge_base = {
            # Geography
            "geography": {
                "capitals": {
                    "france": {"answer": "Paris", "confidence": 0.98, "sources": ["encyclopedia", "atlas"]},
                    "japan": {"answer": "Tokyo", "confidence": 0.98, "sources": ["encyclopedia", "official_data"]},
                    "australia": {"answer": "Canberra", "confidence": 0.95, "sources": ["encyclopedia", "government"]},
                    "germany": {"answer": "Berlin", "confidence": 0.98, "sources": ["encyclopedia", "atlas"]},
                    "italy": {"answer": "Rome", "confidence": 0.98, "sources": ["encyclopedia", "atlas"]},
                    "spain": {"answer": "Madrid", "confidence": 0.97, "sources": ["encyclopedia"]},
                    "canada": {"answer": "Ottawa", "confidence": 0.95, "sources": ["encyclopedia", "government"]},
                    "brazil": {"answer": "Brasília", "confidence": 0.94, "sources": ["encyclopedia"]},
                },
                "landmarks": {
                    "tallest mountain": {"answer": "Mount Everest", "confidence": 0.99, "sources": ["geological_survey", "encyclopedia"]},
                    "longest river": {"answer": "Nile River", "confidence": 0.96, "sources": ["geography_textbook", "atlas"]},
                    "largest desert": {"answer": "Sahara Desert", "confidence": 0.97, "sources": ["geography_textbook"]},
                }
            },
            # Science
            "science": {
                "chemistry": {
                    "gold": {"answer": "Au", "confidence": 0.99, "sources": ["periodic_table", "chemistry_textbook"]},
                    "water": {"answer": "H2O", "confidence": 0.99, "sources": ["chemistry_textbook", "periodic_table"]},
                    "sodium": {"answer": "Na", "confidence": 0.98, "sources": ["periodic_table"]},
                    "oxygen": {"answer": "O", "confidence": 0.99, "sources": ["periodic_table"]},
                },
                "physics": {
                    "speed of light": {"answer": "299,792,458 meters per second", "confidence": 0.99, "sources": ["physics_textbook", "scientific_constants"]},
                    "gravity": {"answer": "9.8 m/s²", "confidence": 0.98, "sources": ["physics_textbook"]},
                },
                "biology": {
                    "fastest land animal": {"answer": "Cheetah", "confidence": 0.97, "sources": ["biology_textbook", "nature_encyclopedia"]},
                    "largest mammal": {"answer": "Blue Whale", "confidence": 0.98, "sources": ["marine_biology", "encyclopedia"]},
                    "human bones": {"answer": "206", "confidence": 0.96, "sources": ["anatomy_textbook", "medical_reference"]},
                }
            },
            # History
            "history": {
                "us_presidents": {
                    "first president": {"answer": "George Washington", "confidence": 0.99, "sources": ["history_textbook", "government_records"]},
                    "president during civil war": {"answer": "Abraham Lincoln", "confidence": 0.99, "sources": ["history_textbook"]},
                },
                "wars": {
                    "world war 2 ended": {"answer": "1945", "confidence": 0.98, "sources": ["history_textbook", "historical_records"]},
                    "world war 1 started": {"answer": "1914", "confidence": 0.97, "sources": ["history_textbook"]},
                },
                "events": {
                    "moon landing": {"answer": "1969", "confidence": 0.99, "sources": ["nasa_records", "history_textbook"]},
                    "berlin wall fell": {"answer": "1989", "confidence": 0.98, "sources": ["history_textbook"]},
                }
            },
            # Mathematics
            "mathematics": {
                "basic": {},  # Will be computed dynamically
                "constants": {
                    "pi": {"answer": "3.14159", "confidence": 0.99, "sources": ["mathematics_textbook"]},
                    "e": {"answer": "2.71828", "confidence": 0.99, "sources": ["mathematics_textbook"]},
                }
            }
        }
        
        # Simulated opponent strategy database
        self.strategy_database = {
            "round_patterns": {
                1: {"rock": 0.5, "paper": 0.3, "scissors": 0.2},  # First round bias toward Rock
                2: {"rock": 0.3, "paper": 0.4, "scissors": 0.3},  # More balanced second round
                3: {"rock": 0.35, "paper": 0.3, "scissors": 0.35}, # Slight Rock preference returns
                4: {"rock": 0.4, "paper": 0.3, "scissors": 0.3},   # Rock preference increases
                5: {"rock": 0.3, "paper": 0.3, "scissors": 0.4},   # Final round unpredictability
            },
            "psychology": {
                "beginner_patterns": ["rock_heavy", "predictable_sequence"],
                "expert_patterns": ["anti_pattern", "random_with_bias"],
                "stress_patterns": ["revert_to_rock", "over_think"]
            }
        }
    
    async def search_knowledge(self, query: str, confidence_threshold: float = 0.7) -> List[Dict]:
        """Simulate vector search across knowledge base"""
        query_lower = query.lower()
        results = []
        
        # Search across all categories
        for category, subcategories in self.knowledge_base.items():
            for subcat, items in subcategories.items():
                for key, data in items.items():
                    if key in query_lower or any(word in key for word in query_lower.split()):
                        if data["confidence"] >= confidence_threshold:
                            results.append({
                                "category": category,
                                "subcategory": subcat,
                                "key": key,
                                "answer": data["answer"],
                                "confidence": data["confidence"],
                                "sources": data["sources"],
                                "relevance_score": self._calculate_relevance(query_lower, key)
                            })
        
        # Handle math questions dynamically
        if any(op in query for op in ["+", "plus", "add", "-", "minus", "subtract", "*", "multiply", "×"]):
            math_result = self._solve_math_question(query)
            if math_result:
                results.append(math_result)
        
        # Sort by relevance and confidence
        results.sort(key=lambda x: (x["relevance_score"], x["confidence"]), reverse=True)
        return results
    
    def _calculate_relevance(self, query: str, key: str) -> float:
        """Calculate relevance score between query and knowledge key"""
        query_words = set(query.lower().split())
        key_words = set(key.lower().split())
        
        if not query_words:
            return 0.0
        
        intersection = query_words.intersection(key_words)
        return len(intersection) / len(query_words)
    
    def _solve_math_question(self, question: str) -> Optional[Dict]:
        """Solve basic math questions dynamically"""
        try:
            import re
            
            # Addition
            if "+" in question or "plus" in question.lower():
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = sum(int(n) for n in numbers)
                    return {
                        "category": "mathematics",
                        "subcategory": "basic",
                        "key": f"addition: {' + '.join(numbers)}",
                        "answer": str(result),
                        "confidence": 0.99,
                        "sources": ["calculation"],
                        "relevance_score": 1.0
                    }
            
            # Subtraction
            if "-" in question or "minus" in question.lower():
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = int(numbers[0]) - int(numbers[1])
                    return {
                        "category": "mathematics", 
                        "subcategory": "basic",
                        "key": f"subtraction: {numbers[0]} - {numbers[1]}",
                        "answer": str(result),
                        "confidence": 0.99,
                        "sources": ["calculation"],
                        "relevance_score": 1.0
                    }
            
            # Multiplication
            if "*" in question or "×" in question or "multiply" in question.lower():
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = int(numbers[0]) * int(numbers[1])
                    return {
                        "category": "mathematics",
                        "subcategory": "basic", 
                        "key": f"multiplication: {numbers[0]} × {numbers[1]}",
                        "answer": str(result),
                        "confidence": 0.99,
                        "sources": ["calculation"],
                        "relevance_score": 1.0
                    }
                    
        except Exception:
            pass
        
        return None
    
    async def get_strategy_data(self, round_number: int) -> Dict:
        """Get strategy data for move selection"""
        base_data = self.strategy_database["round_patterns"].get(round_number, {})
        psychology_data = self.strategy_database["psychology"]
        
        return {
            "round_patterns": base_data,
            "psychology": psychology_data,
            "confidence": 0.85
        }


class AgenticRAGEngine:
    """Core Agentic RAG engine for autonomous retrieval and reasoning"""
    
    def __init__(self, knowledge_base: RPSKnowledgeBase):
        self.kb = knowledge_base
        self.iteration_history = []
        self.max_iterations = 5
        self.confidence_threshold = 0.8
    
    async def answer_question(self, question: str, required_confidence: float = 0.8) -> Dict:
        """
        Agentic RAG process for answering questions with autonomous iteration
        """
        self.iteration_history = []
        
        for iteration in range(self.max_iterations):
            iteration_data = {
                "iteration": iteration + 1,
                "query": question,
                "reasoning": [],
                "sources_consulted": [],
                "confidence": 0.0,
                "answer": None
            }
            
            # Step 1: Initial or refined query
            if iteration == 0:
                search_query = question
                iteration_data["reasoning"].append("Initial question analysis")
            else:
                # Refine query based on previous iterations
                search_query = await self._refine_query(question, iteration)
                iteration_data["reasoning"].append(f"Refined query based on iteration {iteration}")
            
            # Step 2: Knowledge retrieval
            results = await self.kb.search_knowledge(search_query, confidence_threshold=0.5)
            iteration_data["sources_consulted"] = [r["sources"] for r in results]
            
            if not results:
                iteration_data["reasoning"].append("No results found, will try alternative query")
                self.iteration_history.append(iteration_data)
                continue
            
            # Step 3: Evaluate results
            best_result = results[0]  # Highest relevance and confidence
            iteration_data["answer"] = best_result["answer"]
            iteration_data["confidence"] = best_result["confidence"]
            
            # Step 4: Confidence check and decision
            if best_result["confidence"] >= required_confidence:
                iteration_data["reasoning"].append(f"High confidence result found: {best_result['confidence']:.2f}")
                self.iteration_history.append(iteration_data)
                
                return {
                    "answer": best_result["answer"],
                    "confidence": best_result["confidence"],
                    "category": best_result["category"],
                    "sources": best_result["sources"],
                    "iterations": len(self.iteration_history),
                    "reasoning_chain": [h["reasoning"] for h in self.iteration_history],
                    "final_iteration": iteration_data
                }
            
            # Step 5: Self-correction - try different approach
            elif iteration < self.max_iterations - 1:
                iteration_data["reasoning"].append(f"Confidence too low ({best_result['confidence']:.2f}), refining approach")
                
                # Cross-validate with alternative sources if available
                if len(results) > 1:
                    alternative = results[1]
                    if alternative["answer"] == best_result["answer"]:
                        # Multiple sources agree, increase confidence
                        adjusted_confidence = min(0.99, best_result["confidence"] * 1.1)
                        iteration_data["confidence"] = adjusted_confidence
                        iteration_data["reasoning"].append("Multiple sources confirm answer, confidence boosted")
                        
                        if adjusted_confidence >= required_confidence:
                            self.iteration_history.append(iteration_data)
                            return {
                                "answer": best_result["answer"],
                                "confidence": adjusted_confidence,
                                "category": best_result["category"],
                                "sources": best_result["sources"] + alternative["sources"],
                                "iterations": len(self.iteration_history),
                                "reasoning_chain": [h["reasoning"] for h in self.iteration_history],
                                "final_iteration": iteration_data
                            }
            
            self.iteration_history.append(iteration_data)
        
        # Fallback: Return best result even if confidence is low
        if self.iteration_history:
            last_iteration = self.iteration_history[-1]
            return {
                "answer": last_iteration["answer"] or "Unable to find confident answer",
                "confidence": last_iteration["confidence"],
                "category": "unknown",
                "sources": ["knowledge_base"],
                "iterations": len(self.iteration_history),
                "reasoning_chain": [h["reasoning"] for h in self.iteration_history],
                "final_iteration": last_iteration,
                "warning": "Low confidence result"
            }
        
        return {
            "answer": "Unable to answer",
            "confidence": 0.0,
            "category": "unknown",
            "sources": [],
            "iterations": 0,
            "reasoning_chain": [],
            "error": "No results found in any iteration"
        }
    
    async def _refine_query(self, original_question: str, iteration: int) -> str:
        """Refine query based on previous iteration results"""
        question_lower = original_question.lower()
        
        # Different refinement strategies per iteration
        if iteration == 1:
            # Add more specific terms
            if "capital" in question_lower:
                return question_lower + " city government seat"
            elif "chemical" in question_lower:
                return question_lower + " periodic table element symbol"
            elif "largest" in question_lower or "smallest" in question_lower:
                return question_lower + " size comparison facts"
        
        elif iteration == 2:
            # Try alternative phrasings
            if "what is" in question_lower:
                return question_lower.replace("what is", "define")
            elif "chemical symbol" in question_lower:
                return question_lower.replace("chemical symbol", "element abbreviation")
        
        elif iteration == 3:
            # Break down compound questions
            if "?" in question_lower:
                parts = question_lower.split("?")[0]
                key_terms = [word for word in parts.split() if len(word) > 3]
                return " ".join(key_terms[-3:])  # Focus on last few key terms
        
        # Default: return original
        return original_question
    
    async def select_strategic_move(self, round_number: int, current_score: int) -> Dict:
        """Use Agentic RAG for strategic move selection"""
        strategy_data = await self.kb.get_strategy_data(round_number)
        
        reasoning_chain = []
        
        # Analyze round patterns
        round_patterns = strategy_data.get("round_patterns", {})
        if round_patterns:
            most_likely_opponent_move = max(round_patterns, key=round_patterns.get)
            reasoning_chain.append(f"Round {round_number} analysis: opponent likely to play {most_likely_opponent_move.title()}")
            
            # Counter the most likely move
            counters = {"rock": "Paper", "paper": "Scissors", "scissors": "Rock"}
            recommended_move = counters.get(most_likely_opponent_move, "Rock")
            reasoning_chain.append(f"Selected {recommended_move} to counter expected {most_likely_opponent_move.title()}")
        else:
            recommended_move = "Rock"  # Safe default
            reasoning_chain.append("No specific pattern data, defaulting to Rock")
        
        # Adjust for score situation
        if current_score < 0:
            # Behind in score - be more conservative
            recommended_move = "Paper"  # Beats the most common move (Rock)
            reasoning_chain.append("Behind in score: switching to conservative Paper strategy")
        elif current_score > 3:
            # Ahead in score - can afford to be aggressive
            recommended_move = "Rock"  # Show dominance
            reasoning_chain.append("Ahead in score: maintaining aggressive Rock strategy")
        
        return {
            "selected_move": recommended_move,
            "reasoning_chain": reasoning_chain,
            "confidence": strategy_data.get("confidence", 0.7),
            "round_analysis": round_patterns
        }


class GameAgentV3:
    """
    RPS Game Agent V3 - Enhanced with Agentic RAG
    
    This version demonstrates lesson 55 concepts:
    - Agentic Retrieval-Augmented Generation implementation
    - Autonomous query refinement and iteration
    - Self-correction and confidence evaluation
    - Memory and state management across retrieval loops
    """
    
    VERSION = "3.0.0"
    LESSON = "55 - Agentic RAG"
    
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
        
        # Agentic RAG system setup
        self.knowledge_base = RPSKnowledgeBase()
        self.rag_engine = AgenticRAGEngine(self.knowledge_base)
        self.setup_agentic_rag()
        
    def log_status(self, message: str):
        """Add a status message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [V{self.VERSION}] {message}"
        self.status_log.append(log_message)
        print(log_message)
    
    def setup_agentic_rag(self):
        """Initialize the Agentic RAG system"""
        self.log_status(f"Agentic RAG system initialized - Agent V{self.VERSION} ready!")
        self.log_status("RAG capabilities: autonomous iteration, query refinement, confidence evaluation")
    
    async def answer_question_with_rag(self, question: str) -> Tuple[str, Dict]:
        """Use Agentic RAG to answer tournament questions"""
        self.log_status(f"Starting Agentic RAG process for: {question}")
        
        rag_result = await self.rag_engine.answer_question(question, required_confidence=0.8)
        
        # Log the reasoning process
        iterations = rag_result.get("iterations", 0)
        self.log_status(f"RAG completed in {iterations} iterations")
        
        reasoning_chain = rag_result.get("reasoning_chain", [])
        for i, reasoning in enumerate(reasoning_chain, 1):
            self.log_status(f"  Iteration {i}: {', '.join(reasoning)}")
        
        confidence = rag_result.get("confidence", 0.0)
        answer = rag_result.get("answer", "Unknown")
        
        if "warning" in rag_result:
            self.log_status(f"RAG warning: {rag_result['warning']}")
        
        self.log_status(f"RAG result: {answer} (confidence: {confidence:.2f})")
        
        return answer, rag_result
    
    async def select_move_with_rag(self, round_number: int) -> Tuple[str, Dict]:
        """Use Agentic RAG for strategic move selection"""
        self.log_status(f"Starting RAG-based move analysis for round {round_number}")
        
        strategy_result = await self.rag_engine.select_strategic_move(round_number, self.latest_score)
        
        selected_move = strategy_result.get("selected_move", "Rock")
        reasoning = strategy_result.get("reasoning_chain", [])
        
        for reason in reasoning:
            self.log_status(f"  Strategy: {reason}")
        
        confidence = strategy_result.get("confidence", 0.7)
        self.log_status(f"RAG move selection: {selected_move} (confidence: {confidence:.2f})")
        
        return selected_move, strategy_result
    
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
        """Main game loop - monitors status and plays using Agentic RAG"""
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
                    self.log_status(f"Processing Round {current_round} question using Agentic RAG...")
                    
                    # Use Agentic RAG to answer the question
                    answer, rag_result = await self.answer_question_with_rag(question)
                    
                    # Use Agentic RAG for strategic move selection
                    selected_move, strategy_result = await self.select_move_with_rag(current_round)
                    
                    # Submit answer and move
                    rps_move_number = self.get_move_number(selected_move)
                    submit_response = self.client.submit_answer(
                        self.player_id, current_round, answer, rps_move_number
                    )
                    
                    if "error" in submit_response:
                        self.log_status(f"Submission failed: {submit_response['error']}")
                    else:
                        self.log_status(f"Submitted successfully for Round {current_round}")
                        
                        # Log RAG performance metrics
                        iterations = rag_result.get("iterations", 0)
                        confidence = rag_result.get("confidence", 0.0)
                        self.log_status(f"RAG Performance: {iterations} iterations, {confidence:.2f} confidence")
                
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
            correct_answers = sum(1 for result in self.results if result.get("answerCorrect", False))
            accuracy = correct_answers / len(self.results) if self.results else 0
            
            self.log_status(f"Final Results - Total Score: {total_score}, Answer Accuracy: {accuracy:.1%}")
            self.log_status(f"Agent V{self.VERSION} with Agentic RAG tournament complete!")
            
            # RAG performance summary
            self.log_status(f"RAG system provided autonomous reasoning and iterative refinement throughout tournament")
        else:
            self.log_status("No results available")
        
        self.is_running = False


# Usage example for standalone testing
if __name__ == "__main__":
    async def test_agentic_rag():
        agent = GameAgentV3("AI_Agent_V3_RAG")
        
        print(f"Testing Agent V{agent.VERSION} - {agent.LESSON}")
        
        # Test Agentic RAG question answering
        test_questions = [
            "What is the capital of Japan?",
            "What is the chemical symbol for gold?",
            "What is 25 + 17?",
            "What is the fastest land animal?",
            "What is the unknown element X?"  # This should trigger iteration
        ]
        
        for question in test_questions:
            print(f"\nTesting: {question}")
            answer, rag_result = await agent.answer_question_with_rag(question)
            print(f"Answer: {answer}")
            print(f"Confidence: {rag_result.get('confidence', 0.0):.2f}")
            print(f"Iterations: {rag_result.get('iterations', 0)}")
            
            reasoning_chain = rag_result.get('reasoning_chain', [])
            for i, reasoning in enumerate(reasoning_chain, 1):
                print(f"  Iteration {i}: {', '.join(reasoning)}")
        
        # Test RAG-based move selection
        print(f"\nTesting move selection:")
        for round_num in [1, 3, 5]:
            agent.latest_score = round_num - 2  # Simulate score progression
            move, strategy_result = await agent.select_move_with_rag(round_num)
            print(f"Round {round_num}: {move}")
            reasoning = strategy_result.get('reasoning_chain', [])
            for reason in reasoning:
                print(f"  {reason}")
    
    # Run tests
    asyncio.run(test_agentic_rag())