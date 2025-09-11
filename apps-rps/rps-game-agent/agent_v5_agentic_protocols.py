"""
PSR Game Agent V5 - Enhanced with Agentic Protocols (MCP & A2A)
This version demonstrates the concepts from lesson 61 (Agentic Protocols)
- Implements Model Context Protocol (MCP) for tool discovery and execution
- Supports Agent-to-Agent (A2A) protocol for multi-agent collaboration
- Protocol-aware communication with standardized interfaces
- Dynamic tool discovery and interoperability across different systems
"""

import random
import time
import threading
import asyncio
import json
import uuid
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod

# Handle typing for older Python versions
try:
    from typing import Annotated
except ImportError:
    try:
        from typing_extensions import Annotated
    except ImportError:
        def Annotated(type_hint, description):
            return type_hint

from api_client import PSRGameClient


# ==================== MCP Protocol Implementation ====================

@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]


@dataclass
class MCPResource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mime_type: str


@dataclass
class MCPPrompt:
    """MCP Prompt template definition"""
    name: str
    description: str
    template: str
    arguments: List[Dict[str, Any]]


class MCPServer:
    """Simulated MCP Server for PSR Tournament Knowledge"""
    
    def __init__(self, server_name: str):
        self.server_name = server_name
        self.tools = {}
        self.resources = {}
        self.prompts = {}
        self.setup_capabilities()
    
    def setup_capabilities(self):
        """Setup MCP server capabilities for PSR tournament"""
        
        # Register tools
        self.tools["answer_question"] = MCPTool(
            name="answer_question",
            description="Answer tournament questions using knowledge base",
            input_schema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The question to answer"},
                    "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"], "default": "medium"}
                },
                "required": ["question"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "answer": {"type": "string"},
                    "confidence": {"type": "number"},
                    "reasoning": {"type": "string"}
                }
            }
        )
        
        self.tools["analyze_strategy"] = MCPTool(
            name="analyze_strategy",
            description="Analyze optimal Rock, Paper, Scissors strategy",
            input_schema={
                "type": "object",
                "properties": {
                    "round_number": {"type": "integer"},
                    "opponent_history": {"type": "array", "items": {"type": "string"}},
                    "current_score": {"type": "integer"}
                },
                "required": ["round_number"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "recommended_move": {"type": "string"},
                    "confidence": {"type": "number"},
                    "reasoning": {"type": "array", "items": {"type": "string"}}
                }
            }
        )
        
        self.tools["validate_answer"] = MCPTool(
            name="validate_answer",
            description="Validate the correctness of a tournament answer",
            input_schema={
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                    "expected_answer": {"type": "string", "description": "Optional expected answer for comparison"}
                },
                "required": ["question", "answer"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "is_correct": {"type": "boolean"},
                    "confidence": {"type": "number"},
                    "explanation": {"type": "string"}
                }
            }
        )
        
        # Register resources
        self.resources["knowledge_base"] = MCPResource(
            uri="psr://knowledge/general",
            name="General Knowledge Base",
            description="Comprehensive knowledge base for tournament questions",
            mime_type="application/json"
        )
        
        self.resources["strategy_patterns"] = MCPResource(
            uri="psr://strategy/patterns",
            name="Strategy Patterns Database",
            description="Historical patterns and optimal strategies for RPS",
            mime_type="application/json"
        )
        
        # Register prompts
        self.prompts["question_analysis"] = MCPPrompt(
            name="question_analysis",
            description="Analyze a tournament question for optimal answering",
            template="Analyze this tournament question: {question}. Consider difficulty level: {difficulty}. Provide the most accurate answer with reasoning.",
            arguments=[
                {"name": "question", "type": "string", "description": "The question to analyze"},
                {"name": "difficulty", "type": "string", "description": "Question difficulty level"}
            ]
        )
    
    def list_tools(self) -> List[MCPTool]:
        """MCP: List available tools"""
        return list(self.tools.values())
    
    def list_resources(self) -> List[MCPResource]:
        """MCP: List available resources"""
        return list(self.resources.values())
    
    def list_prompts(self) -> List[MCPPrompt]:
        """MCP: List available prompts"""
        return list(self.prompts.values())
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """MCP: Execute a tool with given arguments"""
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
        
        if tool_name == "answer_question":
            return await self._answer_question(arguments)
        elif tool_name == "analyze_strategy":
            return await self._analyze_strategy(arguments)
        elif tool_name == "validate_answer":
            return await self._validate_answer(arguments)
        else:
            return {"error": f"Tool {tool_name} not implemented"}
    
    async def _answer_question(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of answer_question tool"""
        question = args.get("question", "")
        difficulty = args.get("difficulty", "medium")
        
        # Simulate knowledge base lookup
        question_lower = question.lower()
        
        # Geography
        if "capital" in question_lower and "france" in question_lower:
            return {"answer": "Paris", "confidence": 0.98, "reasoning": "Well-established geographical fact"}
        elif "capital" in question_lower and "japan" in question_lower:
            return {"answer": "Tokyo", "confidence": 0.98, "reasoning": "Well-established geographical fact"}
        
        # Science
        elif "chemical symbol" in question_lower and "gold" in question_lower:
            return {"answer": "Au", "confidence": 0.99, "reasoning": "Standard chemical notation from periodic table"}
        elif "largest ocean" in question_lower:
            return {"answer": "Pacific Ocean", "confidence": 0.95, "reasoning": "Geography: Pacific covers ~46% of water surface"}
        
        # Math
        elif "+" in question or "plus" in question_lower:
            try:
                import re
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = sum(int(n) for n in numbers)
                    return {"answer": str(result), "confidence": 0.99, "reasoning": f"Mathematical calculation: {' + '.join(numbers)} = {result}"}
            except:
                pass
        
        return {"answer": "I need more information to answer this question", "confidence": 0.2, "reasoning": "Question not found in knowledge base"}
    
    async def _analyze_strategy(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of analyze_strategy tool"""
        round_number = args.get("round_number", 1)
        opponent_history = args.get("opponent_history", [])
        current_score = args.get("current_score", 0)
        
        reasoning = []
        
        # Round-based strategy
        if round_number == 1:
            recommended_move = "Paper"
            reasoning.append("Round 1: Most beginners choose Rock, counter with Paper")
        elif round_number <= 3:
            recommended_move = "Scissors"
            reasoning.append("Early rounds: People often choose Paper, counter with Scissors")
        else:
            recommended_move = "Rock"
            reasoning.append("Late rounds: Show strength with Rock")
        
        # Score adjustment
        if current_score < -1:
            recommended_move = "Paper"
            reasoning.append("Behind in score: Conservative Paper strategy")
        elif current_score > 2:
            recommended_move = "Rock"
            reasoning.append("Ahead in score: Aggressive Rock strategy")
        
        # Opponent pattern analysis
        if len(opponent_history) >= 2:
            last_moves = opponent_history[-2:]
            if len(set(last_moves)) == 1:  # Pattern detected
                pattern_move = last_moves[0].lower()
                counters = {"rock": "Paper", "paper": "Scissors", "scissors": "Rock"}
                recommended_move = counters.get(pattern_move, recommended_move)
                reasoning.append(f"Opponent pattern detected: {pattern_move}, countering with {recommended_move}")
        
        confidence = 0.8 if len(reasoning) > 2 else 0.6
        
        return {
            "recommended_move": recommended_move,
            "confidence": confidence,
            "reasoning": reasoning
        }
    
    async def _validate_answer(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of validate_answer tool"""
        question = args.get("question", "")
        answer = args.get("answer", "")
        expected = args.get("expected_answer", "")
        
        # Get correct answer using our question answering
        correct_result = await self._answer_question({"question": question})
        correct_answer = correct_result.get("answer", "").lower().strip()
        given_answer = answer.lower().strip()
        
        if correct_answer == given_answer:
            return {"is_correct": True, "confidence": 0.95, "explanation": "Answer matches expected result"}
        elif correct_answer in given_answer or given_answer in correct_answer:
            return {"is_correct": True, "confidence": 0.8, "explanation": "Answer is substantially correct"}
        else:
            return {"is_correct": False, "confidence": 0.9, "explanation": f"Expected: {correct_answer}, Got: {given_answer}"}


# ==================== A2A Protocol Implementation ====================

@dataclass
class AgentCard:
    """A2A Agent Card for agent discovery and capabilities"""
    name: str
    description: str
    skills: List[Dict[str, str]]  # [{"name": "skill_name", "description": "what it does"}]
    endpoint_url: str
    version: str
    capabilities: List[str]  # ["streaming", "push_notifications", etc.]


@dataclass
class A2AArtifact:
    """A2A Artifact containing agent work results"""
    id: str
    agent_name: str
    task_description: str
    result: Dict[str, Any]
    text_context: str
    timestamp: float


@dataclass
class A2ARequest:
    """A2A Request for agent-to-agent communication"""
    id: str
    sender_agent: str
    target_agent: str
    task: str
    context: Dict[str, Any]
    priority: int = 1


class A2AAgent(ABC):
    """Abstract base class for A2A-compatible agents"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.agent_card = self.create_agent_card()
    
    @abstractmethod
    def create_agent_card(self) -> AgentCard:
        """Create agent card describing capabilities"""
        pass
    
    @abstractmethod
    async def execute_task(self, request: A2ARequest) -> A2AArtifact:
        """Execute a task and return an artifact"""
        pass


class PSRQuestionSpecialistA2A(A2AAgent):
    """A2A-compatible Question Specialist Agent"""
    
    def create_agent_card(self) -> AgentCard:
        return AgentCard(
            name="PSR Question Specialist",
            description="Specialized agent for answering PSR tournament questions with high accuracy",
            skills=[
                {"name": "answer_geography", "description": "Answer geography questions (capitals, landmarks, etc.)"},
                {"name": "answer_science", "description": "Answer science questions (chemistry, physics, biology)"},
                {"name": "answer_math", "description": "Solve mathematical problems and calculations"},
                {"name": "answer_history", "description": "Answer historical questions and dates"},
                {"name": "validate_answers", "description": "Validate correctness of provided answers"}
            ],
            endpoint_url="a2a://psr-question-specialist/v1",
            version="1.0.0",
            capabilities=["streaming", "batch_processing", "confidence_scoring"]
        )
    
    async def execute_task(self, request: A2ARequest) -> A2AArtifact:
        task = request.task.lower()
        context = request.context
        
        if "answer" in task and "question" in context:
            question = context["question"]
            # Simulate question answering
            answer_result = await self._answer_question(question)
            
            return A2AArtifact(
                id=str(uuid.uuid4()),
                agent_name=self.agent_name,
                task_description=f"Answered question: {question}",
                result=answer_result,
                text_context=f"Question: {question}\nAnswer: {answer_result['answer']} (confidence: {answer_result['confidence']})",
                timestamp=time.time()
            )
        
        return A2AArtifact(
            id=str(uuid.uuid4()),
            agent_name=self.agent_name,
            task_description="Task not recognized",
            result={"error": "Unknown task"},
            text_context="Unable to process the requested task",
            timestamp=time.time()
        )
    
    async def _answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question using knowledge base"""
        question_lower = question.lower()
        
        if "capital" in question_lower and "france" in question_lower:
            return {"answer": "Paris", "confidence": 0.98, "source": "geography_database"}
        elif "chemical symbol" in question_lower and "gold" in question_lower:
            return {"answer": "Au", "confidence": 0.99, "source": "chemistry_database"}
        elif "+" in question:
            try:
                import re
                numbers = re.findall(r'\d+', question)
                if len(numbers) >= 2:
                    result = sum(int(n) for n in numbers)
                    return {"answer": str(result), "confidence": 0.99, "source": "calculation"}
            except:
                pass
        
        return {"answer": "Unknown", "confidence": 0.1, "source": "fallback"}


class PSRStrategyAnalystA2A(A2AAgent):
    """A2A-compatible Strategy Analyst Agent"""
    
    def create_agent_card(self) -> AgentCard:
        return AgentCard(
            name="PSR Strategy Analyst",
            description="Advanced strategy analysis for Rock, Paper, Scissors gameplay",
            skills=[
                {"name": "analyze_opponent", "description": "Analyze opponent patterns and tendencies"},
                {"name": "recommend_move", "description": "Recommend optimal RPS moves based on game state"},
                {"name": "evaluate_strategy", "description": "Evaluate effectiveness of different strategies"},
                {"name": "predict_outcomes", "description": "Predict likely game outcomes based on current state"}
            ],
            endpoint_url="a2a://psr-strategy-analyst/v1",
            version="1.0.0",
            capabilities=["real_time_analysis", "pattern_recognition", "predictive_modeling"]
        )
    
    async def execute_task(self, request: A2ARequest) -> A2AArtifact:
        task = request.task.lower()
        context = request.context
        
        if "strategy" in task or "move" in task:
            round_number = context.get("round_number", 1)
            opponent_history = context.get("opponent_history", [])
            current_score = context.get("current_score", 0)
            
            strategy_result = await self._analyze_strategy(round_number, opponent_history, current_score)
            
            return A2AArtifact(
                id=str(uuid.uuid4()),
                agent_name=self.agent_name,
                task_description=f"Strategy analysis for round {round_number}",
                result=strategy_result,
                text_context=f"Round {round_number}: Recommend {strategy_result['move']} (confidence: {strategy_result['confidence']})",
                timestamp=time.time()
            )
        
        return A2AArtifact(
            id=str(uuid.uuid4()),
            agent_name=self.agent_name,
            task_description="Task not recognized",
            result={"error": "Unknown task"},
            text_context="Unable to process the requested task",
            timestamp=time.time()
        )
    
    async def _analyze_strategy(self, round_number: int, opponent_history: List[str], current_score: int) -> Dict[str, Any]:
        """Analyze optimal strategy"""
        moves = ["Rock", "Paper", "Scissors"]
        
        if round_number == 1:
            move = "Paper"  # Counter common Rock choice
            reasoning = "First round: counter common Rock choice"
        elif len(opponent_history) >= 2 and len(set(opponent_history[-2:])) == 1:
            # Pattern detected
            last_move = opponent_history[-1].lower()
            counters = {"rock": "Paper", "paper": "Scissors", "scissors": "Rock"}
            move = counters.get(last_move, "Rock")
            reasoning = f"Pattern detected: opponent plays {last_move}, counter with {move}"
        else:
            move = random.choice(moves)
            reasoning = "No clear pattern, random selection"
        
        confidence = 0.8 if "Pattern" in reasoning else 0.6
        
        return {
            "move": move,
            "confidence": confidence,
            "reasoning": reasoning,
            "round_analysis": f"Round {round_number} strategy"
        }


class A2ACoordinator:
    """A2A Coordinator for managing agent interactions"""
    
    def __init__(self):
        self.registered_agents: Dict[str, A2AAgent] = {}
        self.event_queue: List[A2ARequest] = []
        self.artifacts: List[A2AArtifact] = []
    
    def register_agent(self, agent: A2AAgent):
        """Register an A2A agent"""
        self.registered_agents[agent.agent_name] = agent
        print(f"[A2A] Registered agent: {agent.agent_name}")
    
    def list_agents(self) -> List[AgentCard]:
        """List all registered agent cards"""
        return [agent.agent_card for agent in self.registered_agents.values()]
    
    async def send_request(self, request: A2ARequest) -> Optional[A2AArtifact]:
        """Send request to target agent and get artifact"""
        if request.target_agent not in self.registered_agents:
            return None
        
        target_agent = self.registered_agents[request.target_agent]
        artifact = await target_agent.execute_task(request)
        self.artifacts.append(artifact)
        
        return artifact
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get A2A communication statistics"""
        return {
            "registered_agents": len(self.registered_agents),
            "total_requests": len(self.event_queue),
            "artifacts_created": len(self.artifacts),
            "agent_names": list(self.registered_agents.keys())
        }


class GameAgentV5:
    """
    PSR Game Agent V5 - Enhanced with Agentic Protocols (MCP & A2A)
    
    This version demonstrates lesson 61 concepts:
    - Model Context Protocol (MCP) for tool discovery and execution
    - Agent-to-Agent (A2A) protocol for distributed agent collaboration
    - Protocol-aware communication and interoperability
    - Dynamic capability discovery and standardized interfaces
    """
    
    VERSION = "5.0.0"
    LESSON = "61 - Agentic Protocols (MCP & A2A)"
    
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
        
        # Protocol setup
        self.mcp_server = MCPServer("PSR Tournament Knowledge Server")
        self.a2a_coordinator = A2ACoordinator()
        self.setup_protocols()
        
    def log_status(self, message: str):
        """Add a status message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] [V{self.VERSION}] {message}"
        self.status_log.append(log_message)
        print(log_message)
    
    def setup_protocols(self):
        """Initialize MCP and A2A protocols"""
        self.log_status(f"Initializing protocol-aware agent - Agent V{self.VERSION}")
        
        # Setup MCP capabilities
        tools = self.mcp_server.list_tools()
        resources = self.mcp_server.list_resources()
        prompts = self.mcp_server.list_prompts()
        
        self.log_status(f"MCP Server initialized with {len(tools)} tools, {len(resources)} resources, {len(prompts)} prompts")
        
        # Setup A2A agents
        question_agent = PSRQuestionSpecialistA2A("PSR Question Specialist")
        strategy_agent = PSRStrategyAnalystA2A("PSR Strategy Analyst")
        
        self.a2a_coordinator.register_agent(question_agent)
        self.a2a_coordinator.register_agent(strategy_agent)
        
        agent_cards = self.a2a_coordinator.list_agents()
        self.log_status(f"A2A Coordinator initialized with {len(agent_cards)} registered agents")
        
        # Log agent capabilities
        for card in agent_cards:
            self.log_status(f"  - {card.name}: {len(card.skills)} skills, {card.version}")
    
    async def answer_question_with_mcp(self, question: str) -> Tuple[str, Dict]:
        """Use MCP protocol to answer tournament questions"""
        self.log_status(f"[MCP] Requesting question analysis: {question}")
        
        # Discover available tools
        tools = self.mcp_server.list_tools()
        answer_tool = next((t for t in tools if t.name == "answer_question"), None)
        
        if not answer_tool:
            return "No answer tool available", {"error": "MCP tool not found"}
        
        # Call MCP tool
        result = await self.mcp_server.call_tool("answer_question", {
            "question": question,
            "difficulty": "medium"
        })
        
        answer = result.get("answer", "Unknown")
        confidence = result.get("confidence", 0.0)
        reasoning = result.get("reasoning", "No reasoning provided")
        
        self.log_status(f"[MCP] Tool response: {answer} (confidence: {confidence:.2f})")
        self.log_status(f"[MCP] Reasoning: {reasoning}")
        
        return answer, result
    
    async def select_move_with_a2a(self, round_number: int) -> Tuple[str, Dict]:
        """Use A2A protocol to coordinate move selection"""
        self.log_status(f"[A2A] Requesting strategy analysis for round {round_number}")
        
        # Create A2A request
        request = A2ARequest(
            id=str(uuid.uuid4()),
            sender_agent="PSR Tournament Coordinator",
            target_agent="PSR Strategy Analyst",
            task="analyze strategy and recommend move",
            context={
                "round_number": round_number,
                "current_score": self.latest_score,
                "opponent_history": []  # Could be populated with real data
            }
        )
        
        # Send request to A2A agent
        artifact = await self.a2a_coordinator.send_request(request)
        
        if not artifact:
            return "Rock", {"error": "A2A agent not available"}
        
        move = artifact.result.get("move", "Rock")
        confidence = artifact.result.get("confidence", 0.0)
        reasoning = artifact.result.get("reasoning", "No reasoning provided")
        
        self.log_status(f"[A2A] Agent response: {move} (confidence: {confidence:.2f})")
        self.log_status(f"[A2A] Reasoning: {reasoning}")
        self.log_status(f"[A2A] Artifact ID: {artifact.id}")
        
        return move, artifact.result
    
    async def validate_answer_with_mcp(self, question: str, answer: str) -> Dict[str, Any]:
        """Use MCP protocol to validate answers"""
        self.log_status(f"[MCP] Validating answer: {answer} for question: {question}")
        
        result = await self.mcp_server.call_tool("validate_answer", {
            "question": question,
            "answer": answer
        })
        
        is_correct = result.get("is_correct", False)
        confidence = result.get("confidence", 0.0)
        explanation = result.get("explanation", "No explanation")
        
        self.log_status(f"[MCP] Validation: {'Correct' if is_correct else 'Incorrect'} (confidence: {confidence:.2f})")
        self.log_status(f"[MCP] Explanation: {explanation}")
        
        return result
    
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
        """Main game loop - monitors status and plays using protocol-aware agents"""
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
                    self.log_status(f"Processing Round {current_round} using protocol-aware coordination...")
                    self.log_status("=" * 60)
                    
                    # Use MCP protocol for question answering
                    answer, mcp_result = await self.answer_question_with_mcp(question)
                    
                    # Validate answer using MCP
                    validation_result = await self.validate_answer_with_mcp(question, answer)
                    
                    # Use A2A protocol for strategy coordination
                    selected_move, a2a_result = await self.select_move_with_a2a(current_round)
                    
                    self.log_status("=" * 60)
                    self.log_status(f"Protocol coordination complete:")
                    self.log_status(f"  MCP Answer: {answer}")
                    self.log_status(f"  A2A Move: {selected_move}")
                    self.log_status(f"  Validation: {'Passed' if validation_result.get('is_correct') else 'Failed'}")
                    
                    # Submit answer and move
                    rps_move_number = self.get_move_number(selected_move)
                    submit_response = self.client.submit_answer(
                        self.player_id, current_round, answer, rps_move_number
                    )
                    
                    if "error" in submit_response:
                        self.log_status(f"Submission failed: {submit_response['error']}")
                    else:
                        self.log_status(f"Submitted successfully for Round {current_round}")
                        self.log_status(f"Protocol utilization: MCP + A2A coordination successful")
                
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
            
            # Get protocol statistics
            mcp_tools = len(self.mcp_server.list_tools())
            a2a_stats = self.a2a_coordinator.get_communication_stats()
            
            self.log_status(f"Protocol Summary:")
            self.log_status(f"  MCP Tools Used: {mcp_tools}")
            self.log_status(f"  A2A Agents: {a2a_stats['registered_agents']}")
            self.log_status(f"  A2A Artifacts: {a2a_stats['artifacts_created']}")
            
            self.log_status(f"Agent V{self.VERSION} with protocol-aware coordination complete!")
        else:
            self.log_status("No results available")
        
        self.is_running = False


# Usage example for standalone testing
if __name__ == "__main__":
    async def test_protocol_awareness():
        agent = GameAgentV5("AI_Agent_V5_Protocols")
        
        print(f"Testing Agent V{agent.VERSION} - {agent.LESSON}")
        
        # Test MCP protocol
        print("\n=== Testing MCP Protocol ===")
        
        # Test tool discovery
        tools = agent.mcp_server.list_tools()
        print(f"Available MCP tools: {[t.name for t in tools]}")
        
        # Test question answering
        answer, result = await agent.answer_question_with_mcp("What is the capital of France?")
        print(f"MCP Answer: {answer}")
        print(f"MCP Result: {result}")
        
        # Test validation
        validation = await agent.validate_answer_with_mcp("What is the capital of France?", "Paris")
        print(f"MCP Validation: {validation}")
        
        # Test A2A protocol
        print("\n=== Testing A2A Protocol ===")
        
        # Test agent discovery
        agent_cards = agent.a2a_coordinator.list_agents()
        print(f"Available A2A agents: {[c.name for c in agent_cards]}")
        
        # Test strategy coordination
        move, strategy_result = await agent.select_move_with_a2a(3)
        print(f"A2A Move: {move}")
        print(f"A2A Result: {strategy_result}")
        
        # Test direct A2A communication
        print("\n=== Testing Direct A2A Communication ===")
        request = A2ARequest(
            id=str(uuid.uuid4()),
            sender_agent="Test Coordinator",
            target_agent="PSR Question Specialist",
            task="answer question",
            context={"question": "What is the chemical symbol for gold?"}
        )
        
        artifact = await agent.a2a_coordinator.send_request(request)
        if artifact:
            print(f"A2A Artifact: {artifact.text_context}")
            print(f"A2A Result: {artifact.result}")
        
        # Display protocol statistics
        print("\n=== Protocol Statistics ===")
        a2a_stats = agent.a2a_coordinator.get_communication_stats()
        print(f"A2A Statistics: {a2a_stats}")
        
        mcp_capabilities = {
            "tools": len(agent.mcp_server.list_tools()),
            "resources": len(agent.mcp_server.list_resources()),
            "prompts": len(agent.mcp_server.list_prompts())
        }
        print(f"MCP Capabilities: {mcp_capabilities}")
    
    # Run tests
    asyncio.run(test_protocol_awareness())