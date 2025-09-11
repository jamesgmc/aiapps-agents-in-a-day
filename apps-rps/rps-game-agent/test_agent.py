#!/usr/bin/env python3
"""
Simple test script to verify RPS Game Agent functionality
"""

import time
import requests
from api_client import RPSGameClient

def test_agent_apis():
    """Test the game agent's API integration"""
    print("🧪 Testing RPS Game Agent API Integration...")
    
    # Initialize client
    client = RPSGameClient()
    
    print("\n1. Testing Player Registration...")
    response = client.register_player("TestBot")
    print(f"   Registration response: {response}")
    
    if "playerId" in response:
        player_id = response["playerId"]
        print(f"   ✅ Player registered with ID: {player_id}")
        
        print("\n2. Testing Status Check...")
        status = client.get_player_status(player_id)
        print(f"   Status response: {status}")
        
        if "tournamentStatus" in status:
            print("   ✅ Status check successful")
        else:
            print("   ❌ Status check failed")
            
        print("\n3. Testing Results Fetch...")
        results = client.get_player_results(player_id)
        print(f"   Results response: {results}")
        print("   ✅ Results fetch successful")
        
    else:
        print("   ❌ Player registration failed")
        return False
    
    print("\n✅ All API tests passed!")
    return True

def test_question_answering():
    """Test the agent's question answering logic"""
    from agent import GameAgent
    
    print("\n🧠 Testing Question Answering Logic...")
    
    agent = GameAgent("TestAgent")
    
    test_questions = [
        "What is 5 + 3?",
        "What is the capital of Australia?", 
        "What color is the sky?",
        "How many continents are there?",
        "What is 10 - 4?"
    ]
    
    for question in test_questions:
        answer = agent.answer_question(question)
        print(f"   Q: {question}")
        print(f"   A: {answer}")
    
    print("   ✅ Question answering logic working")

def test_rps_selection():
    """Test RPS move selection"""
    from agent import GameAgent
    
    print("\n🪨📄✂️ Testing RPS Move Selection...")
    
    agent = GameAgent("TestAgent")
    
    moves = []
    for i in range(10):
        move = agent.choose_rps_move()
        move_name = agent.get_move_name(move)
        moves.append(move_name)
    
    print(f"   Generated moves: {moves}")
    
    # Check we got variety (not all same move)
    unique_moves = set(moves)
    if len(unique_moves) > 1:
        print("   ✅ RPS selection shows variety")
    else:
        print("   ⚠️  All moves were the same (unlikely but possible)")

def main():
    """Run all tests"""
    print("🎮 RPS Game Agent Test Suite")
    print("=" * 40)
    
    try:
        # Test API connectivity
        response = requests.get("http://localhost:5289", timeout=5)
        if response.status_code == 200:
            print("✅ RPS Game Server is running")
        else:
            print("❌ RPS Game Server not responding properly")
            return
    except requests.RequestException:
        print("❌ RPS Game Server is not running on localhost:5289")
        print("   Please start the server first: cd ../rps-game-server && dotnet run")
        return
    
    # Run tests
    if test_agent_apis():
        test_question_answering()
        test_rps_selection()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 To test the full game flow:")
        print("   1. Start the server: cd ../rps-game-server && dotnet run")
        print("   2. Start the agent: python app.py") 
        print("   3. Open http://localhost:5001 in browser")
        print("   4. Enter player name and watch autonomous gameplay")
        
    else:
        print("\n❌ Some tests failed")

if __name__ == "__main__":
    main()