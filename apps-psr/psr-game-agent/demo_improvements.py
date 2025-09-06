#!/usr/bin/env python3
"""
Demo script to showcase the PSR Game Agent improvements
"""

import time
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent import GameAgent

def demo_agent_features():
    """Demonstrate the enhanced agent features"""
    print("🤖 PSR Game Agent Demo - Enhanced Features")
    print("=" * 50)
    
    # Create a demo agent
    agent = GameAgent("Demo Player")
    
    # Simulate some log entries with enhanced formatting
    agent.log_status("Successfully registered as Player ID: 42")
    agent.log_status("Starting autonomous game monitoring...")
    agent.log_status("Tournament: InProgress, Round 1: InProgress")
    agent.log_status("Processing Round 1 question...")
    agent.log_status("Generated answer: 42")
    agent.log_status("Chosen RPS move: Rock")
    agent.log_status("Successfully submitted answer and move for Round 1")
    
    # Simulate round completion with enhanced formatting
    agent.last_completed_round = 0
    agent.latest_score = 30
    
    # Mock a result entry
    mock_result = {
        "roundNumber": 1,
        "score": 30,
        "answerCorrect": True,
        "move": 0  # Rock
    }
    
    agent.results = [mock_result]
    
    # Simulate getting results (this will trigger the enhanced logging)
    print("\n📊 Simulating round completion...")
    agent.get_current_results()
    
    print(f"\n📋 Agent Status Log ({len(agent.status_log)} entries):")
    for log_entry in agent.status_log[-10:]:  # Show last 10 entries
        print(f"  {log_entry}")
    
    print(f"\n🏆 Results Summary:")
    print(f"  - Rounds completed: {len(agent.results)}")
    print(f"  - Latest score: {agent.latest_score}")
    print(f"  - Total score: {sum(r.get('score', 0) for r in agent.results)}")
    
    print("\n✅ Demo completed! Key improvements:")
    print("  ✨ Enhanced UI with cyberpunk theme")
    print("  🔄 Auto-scrolling activity log")
    print("  🎯 Special round completion effects")
    print("  🔗 Player reconnection functionality")
    print("  📊 Improved score display and animations")

if __name__ == "__main__":
    demo_agent_features()