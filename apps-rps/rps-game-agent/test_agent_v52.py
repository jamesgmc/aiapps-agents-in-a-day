#!/usr/bin/env python3
"""
Simple test to verify agent_v52 interface compatibility
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_agent_interface():
    """Test that agent_v52 has the expected interface"""
    
    print("Testing agent_v52 interface compatibility...")
    
    # Import the agent
    try:
        from agent_v52 import GameAgentV52, GameAgent
        print("✅ Successfully imported GameAgentV52 and GameAgent")
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        return False
    
    # Test instantiation
    try:
        agent = GameAgentV52()
        print("✅ Successfully created GameAgentV52 instance")
    except Exception as e:
        print(f"❌ Failed to create instance: {e}")
        return False
    
    # Test required methods exist
    required_methods = ['answer_question', 'choose_rps_move']
    for method_name in required_methods:
        if hasattr(agent, method_name) and callable(getattr(agent, method_name)):
            print(f"✅ Method {method_name} exists and is callable")
        else:
            print(f"❌ Method {method_name} missing or not callable")
            return False
    
    # Test answer_question method
    try:
        answer = agent.answer_question("What is 2 + 2?")
        print(f"✅ answer_question works, returned: {answer}")
        assert isinstance(answer, str), "answer_question should return a string"
    except Exception as e:
        print(f"❌ answer_question failed: {e}")
        return False
    
    # Test choose_rps_move method
    try:
        move = agent.choose_rps_move()
        print(f"✅ choose_rps_move works, returned: {move}")
        assert isinstance(move, int), "choose_rps_move should return an integer"
        assert 0 <= move <= 2, "choose_rps_move should return 0, 1, or 2"
    except Exception as e:
        print(f"❌ choose_rps_move failed: {e}")
        return False
    
    # Test backward compatibility alias
    try:
        agent_alias = GameAgent()
        print("✅ GameAgent backward compatibility alias works")
    except Exception as e:
        print(f"❌ GameAgent alias failed: {e}")
        return False
    
    print("\n🎉 All interface tests passed! agent_v52 is compatible.")
    return True

if __name__ == "__main__":
    success = test_agent_interface()
    sys.exit(0 if success else 1)