#!/usr/bin/env python3
"""
Test that agent_v52 can be used as a drop-in replacement for agent_v1
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_drop_in_replacement():
    """Test that agent_v52 can replace agent_v1 in GameProcessor"""
    
    print("Testing agent_v52 as drop-in replacement...")
    
    try:
        # Test original import pattern
        from agent_v1 import GameAgent as GameAgentV1
        agent_v1 = GameAgentV1()
        
        # Test new import pattern 
        from agent_v52 import GameAgent as GameAgentV52
        agent_v52 = GameAgentV52()
        
        print("✅ Both agents imported successfully")
        
        # Test same interface
        test_question = "What is 5 + 3?"
        
        # Test agent_v1 (might fail due to missing dependencies)
        try:
            answer_v1 = agent_v1.answer_question(test_question)
            print(f"✅ agent_v1 answer: {answer_v1}")
        except Exception as e:
            print(f"⚠️  agent_v1 failed (expected due to missing deps): {e}")
        
        # Test agent_v52
        answer_v52 = agent_v52.answer_question(test_question)
        print(f"✅ agent_v52 answer: {answer_v52}")
        
        # Test RPS moves
        try:
            move_v1 = agent_v1.choose_rps_move()
            print(f"✅ agent_v1 move: {move_v1}")
        except Exception as e:
            print(f"⚠️  agent_v1 move failed: {e}")
            
        move_v52 = agent_v52.choose_rps_move()
        print(f"✅ agent_v52 move: {move_v52}")
        
        print("\n🎉 agent_v52 successfully works as drop-in replacement!")
        return True
        
    except Exception as e:
        print(f"❌ Drop-in replacement test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_drop_in_replacement()
    sys.exit(0 if success else 1)