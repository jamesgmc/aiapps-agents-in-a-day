#!/usr/bin/env python3
"""
Unit tests for Human-in-the-Loop Agent functionality
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

# Mock the dependencies that might not be available
with patch.dict('sys.modules', {
    'dotenv': Mock(),
    'azure.ai.projects': Mock(),
    'azure.identity': Mock(),
    'azure.ai.agents.models': Mock(),
}):
    from agent_v67 import GameAgentV67


class TestHumanInLoopAgent(unittest.TestCase):
    """Test cases for Human-in-the-Loop Agent functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'PROJECT_ENDPOINT': 'https://test-endpoint.com',
            'MODEL_DEPLOYMENT_NAME': 'test-model',
            'PLAYER_NAME': 'test-player'
        })
        self.env_patcher.start()
        
    def tearDown(self):
        """Clean up test fixtures"""
        self.env_patcher.stop()
    
    @patch('agent_v67.AIProjectClient')
    def test_agent_initialization(self, mock_client):
        """Test agent initialization with human-in-the-loop settings"""
        agent = GameAgentV67()
        
        self.assertEqual(agent.project_endpoint, 'https://test-endpoint.com')
        self.assertEqual(agent.model_deployment_name, 'test-model')
        self.assertEqual(agent.player_name, 'test-player')
        self.assertEqual(agent.agent_name, 'rps-game-agent-human-loop-test-player')
    
    def test_math_tool_function(self):
        """Test the math tool function"""
        # Test successful calculation
        result = GameAgentV67.math_tool_function("2 + 3")
        self.assertEqual(result, "5")
        
        # Test another calculation
        result = GameAgentV67.math_tool_function("10 * 5")
        self.assertEqual(result, "50")
        
        # Test error handling
        result = GameAgentV67.math_tool_function("invalid expression")
        self.assertTrue(result.startswith("Error:"))
    
    @patch('builtins.input', return_value='y')
    def test_human_approval_yes(self, mock_input):
        """Test human approval with 'yes' response"""
        agent = GameAgentV67()
        
        # Mock tool call
        mock_tool_call = Mock()
        mock_tool_call.function.name = "test_function"
        mock_tool_call.function.arguments = '{"param": "value"}'
        mock_tool_call.id = "call_123"
        
        # Test approval
        approved = agent._request_human_approval(mock_tool_call)
        self.assertTrue(approved)
    
    @patch('builtins.input', return_value='n')
    def test_human_approval_no(self, mock_input):
        """Test human approval with 'no' response"""
        agent = GameAgentV67()
        
        # Mock tool call
        mock_tool_call = Mock()
        mock_tool_call.function.name = "test_function"
        mock_tool_call.function.arguments = '{"param": "value"}'
        mock_tool_call.id = "call_123"
        
        # Test rejection
        approved = agent._request_human_approval(mock_tool_call)
        self.assertFalse(approved)
    
    @patch('builtins.input', side_effect=['maybe', 'invalid', 'yes'])
    def test_human_approval_retry_logic(self, mock_input):
        """Test human approval retry logic for invalid responses"""
        agent = GameAgentV67()
        
        # Mock tool call
        mock_tool_call = Mock()
        mock_tool_call.function.name = "test_function"
        mock_tool_call.function.arguments = '{"param": "value"}'
        mock_tool_call.id = "call_123"
        
        # Test that it retries until valid response
        approved = agent._request_human_approval(mock_tool_call)
        self.assertTrue(approved)
        
        # Should have called input 3 times (2 invalid, 1 valid)
        self.assertEqual(mock_input.call_count, 3)
    
    @patch('agent_v67.AIProjectClient')
    def test_setup_tools(self, mock_client):
        """Test tool setup for the agent"""
        agent = GameAgentV67()
        tools = agent._setup_tools()
        
        # Should return tool definitions
        self.assertIsInstance(tools, list)
        # Tools should not be empty (should contain at least math function)
        self.assertGreater(len(tools), 0)
    
    def test_context_manager(self):
        """Test that agent works as context manager"""
        with patch('agent_v67.AIProjectClient') as mock_client:
            mock_client_instance = Mock()
            mock_client.return_value = mock_client_instance
            mock_client_instance.__enter__ = Mock(return_value=mock_client_instance)
            mock_client_instance.__exit__ = Mock(return_value=None)
            
            with GameAgentV67() as agent:
                self.assertIsNotNone(agent)
                # Context manager methods should be called
                mock_client_instance.__enter__.assert_called_once()
            
            mock_client_instance.__exit__.assert_called_once()


class TestHumanInLoopIntegration(unittest.TestCase):
    """Integration tests for human-in-the-loop functionality"""
    
    def test_import_structure(self):
        """Test that all required imports are available"""
        with patch.dict('sys.modules', {
            'dotenv': Mock(),
            'azure.ai.projects': Mock(),
            'azure.identity': Mock(),
            'azure.ai.agents.models': Mock(),
        }):
            from agent_v67 import GameAgentV67, GameAgent
            
            # Test that classes exist
            self.assertTrue(hasattr(GameAgentV67, '_request_human_approval'))
            self.assertTrue(hasattr(GameAgentV67, 'answer_question'))
            self.assertTrue(hasattr(GameAgentV67, 'choose_rps_move'))
            self.assertTrue(hasattr(GameAgentV67, 'math_tool_function'))
            
            # Test backward compatibility alias
            self.assertEqual(GameAgent, GameAgentV67)
    
    def test_demonstration_function_exists(self):
        """Test that demonstration function is available"""
        with patch.dict('sys.modules', {
            'dotenv': Mock(),
            'azure.ai.projects': Mock(),
            'azure.identity': Mock(),
            'azure.ai.agents.models': Mock(),
        }):
            from agent_v67 import demonstrate_human_in_loop
            
            # Function should exist
            self.assertTrue(callable(demonstrate_human_in_loop))


if __name__ == '__main__':
    # Configure test output
    print("🧪 Running Human-in-the-Loop Agent Tests")
    print("=" * 50)
    
    # Run tests
    unittest.main(verbosity=2, buffer=True)