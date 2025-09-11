"""
RPS Game Agent V4 - Enhanced with Multi-Agent Coordination
This version demonstrates the concepts from lesson 58 (Multi-Agent Design Patterns)
- Implements specialized agents for different tournament functions
- Agent communication and coordination mechanisms
- Distributed task handling and collaborative decision making
- Visibility into multi-agent interactions and performance
"""

import random
import time
import threading
import asyncio
import json
import uuid
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum

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


class AgentRole(Enum):
    """Define different agent roles in the multi-agent system"""
    COORDINATOR = "coordinator"
    QUESTION_SPECIALIST = "question_specialist"
    STRATEGY_ANALYST = "strategy_analyst"
    PERFORMANCE_MONITOR = "performance_monitor"
    COMMUNICATION_HUB = "communication_hub"


@dataclass
class AgentMessage:
    """Message structure for inter-agent communication"""
    id: str
    sender: str
    receiver: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    priority: int = 1  # 1 = high, 2 = medium, 3 = low


class MessageBus:
    """Central message bus for agent communication"""
    
    def __init__(self):
        self.message_queue: List[AgentMessage] = []
        self.subscribers: Dict[str, List[str]] = {}  # message_type -> list of agent_ids
        self.message_history: List[AgentMessage] = []
        self.lock = threading.Lock()
    
    def subscribe(self, agent_id: str, message_types: List[str]):
        """Subscribe an agent to specific message types"""
        with self.lock:
            for msg_type in message_types:
                if msg_type not in self.subscribers:
                    self.subscribers[msg_type] = []
                if agent_id not in self.subscribers[msg_type]:
                    self.subscribers[msg_type].append(agent_id)
    
    def publish(self, message: AgentMessage):
        """Publish a message to the bus"""
        with self.lock:
            self.message_queue.append(message)
            self.message_history.append(message)
            # Sort by priority and timestamp
            self.message_queue.sort(key=lambda x: (x.priority, x.timestamp))
    
    def get_messages_for_agent(self, agent_id: str) -> List[AgentMessage]:
        """Get all pending messages for a specific agent"""
        with self.lock:
            messages = []
            remaining_queue = []
            
            for msg in self.message_queue:
                if msg.receiver == agent_id or msg.receiver == "ALL":
                    messages.append(msg)
                else:
                    # Check if agent is subscribed to this message type
                    subscribers = self.subscribers.get(msg.message_type, [])
                    if agent_id in subscribers:
                        messages.append(msg)
                    else:
                        remaining_queue.append(msg)
            
            self.message_queue = remaining_queue
            return messages
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get statistics about inter-agent communication"""
        with self.lock:
            total_messages = len(self.message_history)
            message_types = {}
            agent_activity = {}
            
            for msg in self.message_history:
                message_types[msg.message_type] = message_types.get(msg.message_type, 0) + 1
                agent_activity[msg.sender] = agent_activity.get(msg.sender, 0) + 1
            
            return {
                "total_messages": total_messages,
                "message_types": message_types,
                "agent_activity": agent_activity,
                "active_agents": len(agent_activity)
            }


class BaseAgent:
    """Base class for all agents in the multi-agent system"""
    
    def __init__(self, agent_id: str, role: AgentRole, message_bus: MessageBus):
        self.agent_id = agent_id
        self.role = role
        self.message_bus = message_bus
        self.is_active = False
        self.status = "initialized"
        self.performance_metrics = {
            "messages_sent": 0,
            "messages_received": 0,
            "tasks_completed": 0,
            "uptime_start": None
        }
        
    def start(self):
        """Start the agent"""
        self.is_active = True
        self.status = "active"
        self.performance_metrics["uptime_start"] = time.time()
        self.log(f"Agent {self.agent_id} ({self.role.value}) started")
    
    def stop(self):
        """Stop the agent"""
        self.is_active = False
        self.status = "stopped"
        self.log(f"Agent {self.agent_id} ({self.role.value}) stopped")
    
    def log(self, message: str):
        """Log agent activity"""
        timestamp = time.strftime("%H:%M:%S")
        print(f"[{timestamp}] [{self.agent_id}] {message}")
    
    def send_message(self, receiver: str, message_type: str, payload: Dict[str, Any], priority: int = 1):
        """Send a message to another agent"""
        message = AgentMessage(
            id=str(uuid.uuid4()),
            sender=self.agent_id,
            receiver=receiver,
            message_type=message_type,
            payload=payload,
            timestamp=time.time(),
            priority=priority
        )
        self.message_bus.publish(message)
        self.performance_metrics["messages_sent"] += 1
        self.log(f"Sent {message_type} to {receiver}")
    
    def process_messages(self):
        """Process incoming messages"""
        messages = self.message_bus.get_messages_for_agent(self.agent_id)
        for message in messages:
            self.performance_metrics["messages_received"] += 1
            self.handle_message(message)
    
    def handle_message(self, message: AgentMessage):
        """Handle incoming message - to be overridden by subclasses"""
        pass
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        metrics = self.performance_metrics.copy()
        if metrics["uptime_start"]:
            metrics["uptime_seconds"] = time.time() - metrics["uptime_start"]
        return metrics


class QuestionSpecialistAgent(BaseAgent):
    """Agent specialized in answering tournament questions"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentRole.QUESTION_SPECIALIST, message_bus)
        
        # Subscribe to question-related messages
        self.message_bus.subscribe(agent_id, ["question_request", "answer_validation"])
        
        # Knowledge base for quick question answering
        self.knowledge_cache = {
            "capitals": {"france": "Paris", "japan": "Tokyo", "australia": "Canberra"},
            "science": {"gold": "Au", "water": "H2O", "largest_ocean": "Pacific Ocean"},
            "math": {},  # Will compute dynamically
        }
    
    def handle_message(self, message: AgentMessage):
        """Handle incoming messages"""
        if message.message_type == "question_request":
            self.handle_question_request(message)
        elif message.message_type == "answer_validation":
            self.handle_answer_validation(message)
    
    def handle_question_request(self, message: AgentMessage):
        """Handle question answering requests"""
        question = message.payload.get("question", "")
        round_number = message.payload.get("round_number", 1)
        
        self.log(f"Processing question: {question}")
        
        # Analyze question and provide answer
        answer_result = self.analyze_question(question)
        
        # Send response back to coordinator
        self.send_message(
            receiver=message.sender,
            message_type="question_response",
            payload={
                "question": question,
                "answer": answer_result["answer"],
                "confidence": answer_result["confidence"],
                "reasoning": answer_result["reasoning"],
                "round_number": round_number
            },
            priority=1
        )
        
        self.performance_metrics["tasks_completed"] += 1
    
    def analyze_question(self, question: str) -> Dict[str, Any]:
        """Analyze and answer the question"""
        question_lower = question.lower()
        
        # Geography questions
        if "capital" in question_lower:
            for country, capital in self.knowledge_cache["capitals"].items():
                if country in question_lower:
                    return {
                        "answer": capital,
                        "confidence": 0.95,
                        "reasoning": f"Found {country} in knowledge cache"
                    }
        
        # Science questions
        if "chemical symbol" in question_lower or "symbol for" in question_lower:
            for element, symbol in self.knowledge_cache["science"].items():
                if element in question_lower:
                    return {
                        "answer": symbol,
                        "confidence": 0.98,
                        "reasoning": f"Chemical symbol lookup for {element}"
                    }
        
        # Math questions
        if any(op in question for op in ["+", "plus", "-", "minus"]):
            try:
                import re
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    if "+" in question or "plus" in question_lower:
                        result = sum(int(n) for n in numbers)
                        return {
                            "answer": str(result),
                            "confidence": 0.99,
                            "reasoning": f"Mathematical calculation: {' + '.join(numbers)} = {result}"
                        }
            except:
                pass
        
        # Default response
        return {
            "answer": "I need to research this question",
            "confidence": 0.3,
            "reasoning": "Question not found in specialized knowledge base"
        }
    
    def handle_answer_validation(self, message: AgentMessage):
        """Validate an answer"""
        answer = message.payload.get("answer", "")
        question = message.payload.get("question", "")
        
        validation_result = self.validate_answer(question, answer)
        
        self.send_message(
            receiver=message.sender,
            message_type="validation_response",
            payload={
                "question": question,
                "answer": answer,
                "is_valid": validation_result["is_valid"],
                "confidence": validation_result["confidence"],
                "suggestions": validation_result.get("suggestions", [])
            }
        )
    
    def validate_answer(self, question: str, answer: str) -> Dict[str, Any]:
        """Validate an answer against the question"""
        expected_result = self.analyze_question(question)
        expected_answer = expected_result["answer"].lower().strip()
        given_answer = answer.lower().strip()
        
        if expected_answer == given_answer:
            return {"is_valid": True, "confidence": 0.95}
        elif expected_answer in given_answer or given_answer in expected_answer:
            return {"is_valid": True, "confidence": 0.8, "suggestions": ["Answer is close but could be more precise"]}
        else:
            return {"is_valid": False, "confidence": 0.1, "suggestions": [f"Expected answer: {expected_result['answer']}"]}


class StrategyAnalystAgent(BaseAgent):
    """Agent specialized in analyzing optimal moves and strategies"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentRole.STRATEGY_ANALYST, message_bus)
        
        # Subscribe to strategy-related messages
        self.message_bus.subscribe(agent_id, ["strategy_request", "opponent_analysis"])
        
        # Strategy database
        self.strategy_patterns = {
            1: {"rock": 0.5, "paper": 0.3, "scissors": 0.2},  # Round 1 patterns
            2: {"rock": 0.3, "paper": 0.4, "scissors": 0.3},
            3: {"rock": 0.35, "paper": 0.3, "scissors": 0.35},
            4: {"rock": 0.4, "paper": 0.3, "scissors": 0.3},
            5: {"rock": 0.3, "paper": 0.3, "scissors": 0.4},
        }
    
    def handle_message(self, message: AgentMessage):
        """Handle incoming messages"""
        if message.message_type == "strategy_request":
            self.handle_strategy_request(message)
        elif message.message_type == "opponent_analysis":
            self.handle_opponent_analysis(message)
    
    def handle_strategy_request(self, message: AgentMessage):
        """Handle strategy analysis requests"""
        round_number = message.payload.get("round_number", 1)
        current_score = message.payload.get("current_score", 0)
        opponent_history = message.payload.get("opponent_history", [])
        
        self.log(f"Analyzing strategy for round {round_number}")
        
        strategy_result = self.analyze_strategy(round_number, current_score, opponent_history)
        
        # Send response back to coordinator
        self.send_message(
            receiver=message.sender,
            message_type="strategy_response",
            payload={
                "round_number": round_number,
                "recommended_move": strategy_result["move"],
                "confidence": strategy_result["confidence"],
                "reasoning": strategy_result["reasoning"],
                "alternative_moves": strategy_result.get("alternatives", [])
            },
            priority=1
        )
        
        self.performance_metrics["tasks_completed"] += 1
    
    def analyze_strategy(self, round_number: int, current_score: int, opponent_history: List[str]) -> Dict[str, Any]:
        """Analyze optimal strategy for the given situation"""
        reasoning = []
        
        # Get round-specific patterns
        round_patterns = self.strategy_patterns.get(round_number, {"rock": 0.33, "paper": 0.33, "scissors": 0.34})
        most_likely_opponent = max(round_patterns, key=round_patterns.get)
        reasoning.append(f"Round {round_number}: opponent likely to play {most_likely_opponent.title()}")
        
        # Counter logic
        counters = {"rock": "Paper", "paper": "Scissors", "scissors": "Rock"}
        recommended_move = counters[most_likely_opponent]
        reasoning.append(f"Countering with {recommended_move}")
        
        # Adjust for score situation
        confidence = 0.8
        if current_score < -1:
            # Losing - be more conservative
            recommended_move = "Paper"  # Safest choice
            reasoning.append("Behind in score: switching to conservative Paper")
            confidence = 0.7
        elif current_score > 2:
            # Winning - maintain pressure
            recommended_move = "Rock"  # Show dominance
            reasoning.append("Ahead in score: maintaining aggressive stance")
            confidence = 0.85
        
        # Factor in opponent history if available
        if opponent_history and len(opponent_history) >= 2:
            recent_moves = opponent_history[-2:]
            if len(set(recent_moves)) == 1:  # Opponent is being predictable
                predictable_move = recent_moves[0]
                counter_move = counters.get(predictable_move.lower(), recommended_move)
                reasoning.append(f"Opponent showing pattern: {predictable_move}, countering with {counter_move}")
                recommended_move = counter_move
                confidence = 0.9
        
        return {
            "move": recommended_move,
            "confidence": confidence,
            "reasoning": reasoning,
            "alternatives": [move for move in ["Rock", "Paper", "Scissors"] if move != recommended_move]
        }
    
    def handle_opponent_analysis(self, message: AgentMessage):
        """Analyze opponent patterns"""
        move_history = message.payload.get("move_history", [])
        analysis = self.analyze_opponent_patterns(move_history)
        
        self.send_message(
            receiver=message.sender,
            message_type="opponent_analysis_response",
            payload=analysis
        )
    
    def analyze_opponent_patterns(self, move_history: List[str]) -> Dict[str, Any]:
        """Analyze opponent move patterns"""
        if not move_history:
            return {"pattern": "no_data", "confidence": 0.0}
        
        move_counts = {"rock": 0, "paper": 0, "scissors": 0}
        for move in move_history:
            move_lower = move.lower()
            if move_lower in move_counts:
                move_counts[move_lower] += 1
        
        total_moves = len(move_history)
        move_percentages = {move: count/total_moves for move, count in move_counts.items()}
        
        # Determine pattern type
        max_percentage = max(move_percentages.values())
        if max_percentage > 0.6:
            pattern = "predictable"
            confidence = 0.8
        elif max_percentage > 0.4:
            pattern = "biased"
            confidence = 0.6
        else:
            pattern = "random"
            confidence = 0.4
        
        return {
            "pattern": pattern,
            "confidence": confidence,
            "move_distribution": move_percentages,
            "sample_size": total_moves
        }


class PerformanceMonitorAgent(BaseAgent):
    """Agent specialized in monitoring system and tournament performance"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        super().__init__(agent_id, AgentRole.PERFORMANCE_MONITOR, message_bus)
        
        # Subscribe to performance-related messages
        self.message_bus.subscribe(agent_id, ["performance_request", "round_completed", "tournament_update"])
        
        self.performance_data = {
            "rounds_completed": 0,
            "total_score": 0,
            "answer_accuracy": 0.0,
            "move_success_rate": 0.0,
            "system_metrics": {
                "response_times": [],
                "error_count": 0,
                "uptime": 0
            }
        }
    
    def handle_message(self, message: AgentMessage):
        """Handle incoming messages"""
        if message.message_type == "performance_request":
            self.handle_performance_request(message)
        elif message.message_type == "round_completed":
            self.handle_round_completed(message)
        elif message.message_type == "tournament_update":
            self.handle_tournament_update(message)
    
    def handle_performance_request(self, message: AgentMessage):
        """Handle performance analysis requests"""
        self.log("Generating performance report")
        
        # Calculate current performance metrics
        performance_report = self.generate_performance_report()
        
        self.send_message(
            receiver=message.sender,
            message_type="performance_response",
            payload=performance_report,
            priority=2
        )
        
        self.performance_metrics["tasks_completed"] += 1
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        # Get communication stats from message bus
        comm_stats = self.message_bus.get_communication_stats()
        
        return {
            "tournament_performance": self.performance_data,
            "communication_stats": comm_stats,
            "system_health": {
                "active_agents": comm_stats["active_agents"],
                "message_throughput": comm_stats["total_messages"],
                "error_rate": self.performance_data["system_metrics"]["error_count"]
            },
            "recommendations": self.generate_recommendations()
        }
    
    def generate_recommendations(self) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        
        if self.performance_data["answer_accuracy"] < 0.7:
            recommendations.append("Consider improving question answering accuracy")
        
        if self.performance_data["move_success_rate"] < 0.5:
            recommendations.append("Strategy analysis may need adjustment")
        
        if len(self.performance_data["system_metrics"]["response_times"]) > 0:
            avg_response_time = sum(self.performance_data["system_metrics"]["response_times"]) / len(self.performance_data["system_metrics"]["response_times"])
            if avg_response_time > 2.0:
                recommendations.append("System response times are high")
        
        if not recommendations:
            recommendations.append("System performing within normal parameters")
        
        return recommendations
    
    def handle_round_completed(self, message: AgentMessage):
        """Handle round completion updates"""
        round_data = message.payload
        
        self.performance_data["rounds_completed"] += 1
        self.performance_data["total_score"] += round_data.get("score", 0)
        
        if round_data.get("answer_correct"):
            # Update answer accuracy
            rounds = self.performance_data["rounds_completed"]
            current_accuracy = self.performance_data["answer_accuracy"]
            self.performance_data["answer_accuracy"] = (current_accuracy * (rounds - 1) + 1) / rounds
        
        self.log(f"Updated performance data for round {round_data.get('round_number', '?')}")
    
    def handle_tournament_update(self, message: AgentMessage):
        """Handle general tournament updates"""
        update_data = message.payload
        response_time = update_data.get("response_time", 0)
        
        if response_time > 0:
            self.performance_data["system_metrics"]["response_times"].append(response_time)
            # Keep only last 10 response times
            if len(self.performance_data["system_metrics"]["response_times"]) > 10:
                self.performance_data["system_metrics"]["response_times"].pop(0)


class TournamentCoordinatorAgent(BaseAgent):
    """Main coordinator agent that orchestrates the multi-agent system"""
    
    def __init__(self, agent_id: str, message_bus: MessageBus, client: RPSGameClient):
        super().__init__(agent_id, AgentRole.COORDINATOR, message_bus)
        
        self.client = client
        self.player_id: Optional[int] = None
        self.current_round = 1
        self.latest_score = 0
        self.tournament_status = "Not Started"
        
        # Track agent responses
        self.pending_requests = {}
        
        # Subscribe to all response messages
        self.message_bus.subscribe(agent_id, [
            "question_response", "strategy_response", "performance_response",
            "validation_response", "opponent_analysis_response"
        ])
    
    def handle_message(self, message: AgentMessage):
        """Handle incoming messages from other agents"""
        request_id = message.payload.get("round_number", message.payload.get("request_id"))
        
        if message.message_type in ["question_response", "strategy_response"]:
            self.pending_requests[message.message_type] = message.payload
            self.log(f"Received {message.message_type} for round {request_id}")
        elif message.message_type == "performance_response":
            self.log("Received performance report")
            self.display_performance_report(message.payload)
    
    def display_performance_report(self, report: Dict[str, Any]):
        """Display performance report"""
        self.log("=== PERFORMANCE REPORT ===")
        
        tournament_perf = report.get("tournament_performance", {})
        self.log(f"Rounds completed: {tournament_perf.get('rounds_completed', 0)}")
        self.log(f"Total score: {tournament_perf.get('total_score', 0)}")
        self.log(f"Answer accuracy: {tournament_perf.get('answer_accuracy', 0.0):.2f}")
        
        comm_stats = report.get("communication_stats", {})
        self.log(f"Total messages: {comm_stats.get('total_messages', 0)}")
        self.log(f"Active agents: {comm_stats.get('active_agents', 0)}")
        
        recommendations = report.get("recommendations", [])
        self.log("Recommendations:")
        for rec in recommendations:
            self.log(f"  - {rec}")
    
    async def coordinate_tournament_round(self, question: str, round_number: int) -> Tuple[str, str]:
        """Coordinate a tournament round using multiple agents"""
        start_time = time.time()
        
        self.log(f"=== COORDINATING ROUND {round_number} ===")
        
        # Clear pending requests
        self.pending_requests = {}
        
        # Request question analysis from specialist
        self.send_message(
            receiver="question_specialist",
            message_type="question_request",
            payload={
                "question": question,
                "round_number": round_number
            },
            priority=1
        )
        
        # Request strategy analysis
        self.send_message(
            receiver="strategy_analyst",
            message_type="strategy_request",
            payload={
                "round_number": round_number,
                "current_score": self.latest_score,
                "opponent_history": []  # Could be populated with actual data
            },
            priority=1
        )
        
        # Wait for responses from both agents
        max_wait_time = 5.0  # 5 seconds max
        wait_start = time.time()
        
        while len(self.pending_requests) < 2 and (time.time() - wait_start) < max_wait_time:
            self.process_messages()
            await asyncio.sleep(0.1)
        
        # Get results
        question_result = self.pending_requests.get("question_response", {})
        strategy_result = self.pending_requests.get("strategy_response", {})
        
        answer = question_result.get("answer", "Unknown")
        move = strategy_result.get("recommended_move", "Rock")
        
        # Log coordination results
        response_time = time.time() - start_time
        self.log(f"Coordination completed in {response_time:.2f}s")
        self.log(f"Question: {question}")
        self.log(f"Answer: {answer} (confidence: {question_result.get('confidence', 0.0):.2f})")
        self.log(f"Move: {move} (confidence: {strategy_result.get('confidence', 0.0):.2f})")
        
        # Log reasoning
        question_reasoning = question_result.get("reasoning", "")
        if question_reasoning:
            self.log(f"Question reasoning: {question_reasoning}")
        
        strategy_reasoning = strategy_result.get("reasoning", [])
        if strategy_reasoning:
            self.log(f"Strategy reasoning: {'; '.join(strategy_reasoning)}")
        
        # Notify performance monitor
        self.send_message(
            receiver="performance_monitor",
            message_type="tournament_update",
            payload={
                "round_number": round_number,
                "response_time": response_time
            },
            priority=3
        )
        
        return answer, move
    
    async def request_performance_report(self):
        """Request performance report from monitor agent"""
        self.send_message(
            receiver="performance_monitor",
            message_type="performance_request",
            payload={"timestamp": time.time()},
            priority=2
        )
        
        # Wait for response
        await asyncio.sleep(0.5)
        self.process_messages()


class GameAgentV4:
    """
    RPS Game Agent V4 - Enhanced with Multi-Agent Coordination
    
    This version demonstrates lesson 58 concepts:
    - Multi-agent design patterns implementation
    - Specialized agents for different functions
    - Agent communication and coordination
    - Visibility into multi-agent interactions
    """
    
    VERSION = "4.0.0"
    LESSON = "58 - Multi-Agent Design Patterns"
    
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
        
        # Multi-agent system setup
        self.message_bus = MessageBus()
        self.agents: Dict[str, BaseAgent] = {}
        self.setup_multi_agent_system()
        
    def log_status(self, message: str):
        """Add a status message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [V{self.VERSION}] {message}"
        self.status_log.append(log_message)
        print(log_message)
    
    def setup_multi_agent_system(self):
        """Initialize the multi-agent system"""
        self.log_status(f"Initializing multi-agent system - Agent V{self.VERSION}")
        
        # Create specialized agents
        self.agents["coordinator"] = TournamentCoordinatorAgent("coordinator", self.message_bus, self.client)
        self.agents["question_specialist"] = QuestionSpecialistAgent("question_specialist", self.message_bus)
        self.agents["strategy_analyst"] = StrategyAnalystAgent("strategy_analyst", self.message_bus)
        self.agents["performance_monitor"] = PerformanceMonitorAgent("performance_monitor", self.message_bus)
        
        # Start all agents
        for agent_id, agent in self.agents.items():
            agent.start()
            self.log_status(f"Started {agent_id} agent ({agent.role.value})")
        
        self.log_status("Multi-agent system operational")
        self.log_status(f"Active agents: {len(self.agents)}")
    
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
            self.agents["coordinator"].player_id = self.player_id
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
        """Main game loop - monitors status and plays using multi-agent coordination"""
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
                coordinator = self.agents["coordinator"]
                coordinator.current_round = current_round
                coordinator.latest_score = self.latest_score
                
                # Handle different states
                if tournament_status == 2:  # Completed
                    self.log_status("Tournament completed!")
                    await self.get_final_results()
                    break
                
                if tournament_status == 1 and round_status == 1 and can_submit and question:
                    # Round is in progress and we can submit
                    self.log_status(f"Processing Round {current_round} using multi-agent coordination...")
                    
                    # Use multi-agent system to coordinate response
                    answer, selected_move = await coordinator.coordinate_tournament_round(question, current_round)
                    
                    # Submit answer and move
                    rps_move_number = self.get_move_number(selected_move)
                    submit_response = self.client.submit_answer(
                        self.player_id, current_round, answer, rps_move_number
                    )
                    
                    if "error" in submit_response:
                        self.log_status(f"Submission failed: {submit_response['error']}")
                    else:
                        self.log_status(f"Submitted successfully for Round {current_round}")
                        self.log_status(f"Multi-agent coordination: {len(self.agents)} agents collaborated")
                
                # Process messages for all agents
                for agent in self.agents.values():
                    agent.process_messages()
                
                # Get current results
                await self.get_current_results()
                
                # Request performance report every few rounds
                if current_round > 1 and current_round % 2 == 0:
                    await coordinator.request_performance_report()
                
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
                
                # Notify performance monitor about round completion
                performance_monitor = self.agents.get("performance_monitor")
                if performance_monitor:
                    performance_monitor.send_message(
                        receiver="performance_monitor",
                        message_type="round_completed",
                        payload={
                            "round_number": round_num,
                            "score": score,
                            "answer_correct": latest_result.get("answerCorrect", False)
                        }
                    )
    
    async def get_final_results(self):
        """Get and display final tournament results"""
        await self.get_current_results()
        
        if self.results:
            total_score = sum(result.get("score", 0) for result in self.results)
            correct_answers = sum(1 for result in self.results if result.get("answerCorrect", False))
            accuracy = correct_answers / len(self.results) if self.results else 0
            
            self.log_status(f"Final Results - Total Score: {total_score}, Answer Accuracy: {accuracy:.1%}")
            
            # Get final performance report
            coordinator = self.agents["coordinator"]
            await coordinator.request_performance_report()
            
            # Get communication statistics
            comm_stats = self.message_bus.get_communication_stats()
            self.log_status(f"Communication Summary:")
            self.log_status(f"  Total messages: {comm_stats['total_messages']}")
            self.log_status(f"  Active agents: {comm_stats['active_agents']}")
            self.log_status(f"  Message types: {list(comm_stats['message_types'].keys())}")
            
            self.log_status(f"Agent V{self.VERSION} multi-agent tournament complete!")
        else:
            self.log_status("No results available")
        
        # Stop all agents
        for agent in self.agents.values():
            agent.stop()
        
        self.is_running = False


# Usage example for standalone testing
if __name__ == "__main__":
    async def test_multi_agent_system():
        game_agent = GameAgentV4("AI_Agent_V4_MultiAgent")
        
        print(f"Testing Agent V{game_agent.VERSION} - {game_agent.LESSON}")
        
        # Test individual agent communication
        coordinator = game_agent.agents["coordinator"]
        
        # Test question answering agent
        print("\n=== Testing Question Specialist ===")
        coordinator.send_message(
            receiver="question_specialist",
            message_type="question_request",
            payload={"question": "What is the capital of Japan?", "round_number": 1}
        )
        
        # Test strategy analyst agent
        print("\n=== Testing Strategy Analyst ===")
        coordinator.send_message(
            receiver="strategy_analyst",
            message_type="strategy_request",
            payload={"round_number": 3, "current_score": 2, "opponent_history": ["Rock", "Paper"]}
        )
        
        # Process messages
        await asyncio.sleep(1)
        for agent_instance in game_agent.agents.values():
            agent_instance.process_messages()
        
        # Test performance monitoring
        print("\n=== Testing Performance Monitor ===")
        coordinator.send_message(
            receiver="performance_monitor",
            message_type="performance_request",
            payload={"timestamp": time.time()}
        )
        
        await asyncio.sleep(1)
        for agent_instance in game_agent.agents.values():
            agent_instance.process_messages()
        
        # Test full coordination
        print("\n=== Testing Full Coordination ===")
        answer, move = await coordinator.coordinate_tournament_round(
            "What is the chemical symbol for gold?", 2
        )
        print(f"Coordinated result: Answer={answer}, Move={move}")
        
        # Display final statistics
        print("\n=== Communication Statistics ===")
        stats = game_agent.message_bus.get_communication_stats()
        print(f"Total messages: {stats['total_messages']}")
        print(f"Message types: {stats['message_types']}")
        print(f"Agent activity: {stats['agent_activity']}")
        
        # Stop all agents
        for agent_instance in game_agent.agents.values():
            agent_instance.stop()
    
    # Run tests
    asyncio.run(test_multi_agent_system())