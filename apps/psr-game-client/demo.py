#!/usr/bin/env python3
"""
Demo script showing PSR Game Client functionality
"""

import time
import random
from psr_game_client import PSRGameClient


def random_move():
    """Generate random move for demo"""
    return random.choice(['rock', 'paper', 'scissors'])


def demo_client_features():
    """Demonstrate all client features"""
    print("🎮 PSR Game Client Demo")
    print("======================")
    
    # Initialize client
    client = PSRGameClient()
    print(f"📡 Connected to server: {client.server_url}")
    
    # Demo 1: Tournament Status Check
    print("\n1️⃣ Checking Tournament Status...")
    state = client.get_tournament_state()
    if state:
        status_names = ['WaitingForPlayers', 'InProgress', 'Completed']
        print(f"   Tournament ID: {state.get('tournamentId')}")
        print(f"   Status: {status_names[state.get('status', 0)]}")
        print(f"   Players: {len(state.get('players', []))}/8")
        print(f"   Current Round: {state.get('currentRound', 1)}")
    else:
        print("   No active tournament found")
    
    # Demo 2: Player Registration
    print("\n2️⃣ Registering Demo Player...")
    player_name = f"DemoPlayer_{int(time.time())}"
    if client.register_player(player_name):
        print(f"   ✅ Successfully registered as '{player_name}'")
        print(f"   Player ID: {client.player_id}")
        print(f"   Tournament ID: {client.tournament_id}")
    else:
        print("   ❌ Registration failed")
        return
    
    # Demo 3: Updated Tournament Status
    print("\n3️⃣ Updated Tournament Status...")
    state = client.get_tournament_state()
    if state:
        print(f"   Players now: {len(state.get('players', []))}/8")
        players_needed = 8 - len(state.get('players', []))
        if players_needed > 0:
            print(f"   Waiting for {players_needed} more players to start tournament")
        else:
            print("   Tournament ready to start!")
    
    # Demo 4: Current Match Check
    print("\n4️⃣ Checking for Current Match...")
    match = client.get_current_match()
    if match:
        print(f"   Active match found: Round {match.get('round')}")
        print(f"   Match ID: {match.get('id')}")
        opponent = match.get('player2') if match.get('player1', {}).get('id') == client.player_id else match.get('player1')
        if opponent:
            print(f"   Opponent: {opponent.get('name')}")
    else:
        print("   No active match (expected - tournament not started)")
    
    # Demo 5: Move Validation
    print("\n5️⃣ Testing Move Validation...")
    valid_moves = ['rock', 'paper', 'scissors']
    test_move = random.choice(valid_moves)
    print(f"   Testing move: {test_move}")
    result = client.submit_move(test_move)
    if result:
        print("   ✅ Move accepted")
    else:
        print("   ❌ Move rejected (expected - no active match)")
    
    # Demo 6: Invalid move test
    print("\n6️⃣ Testing Invalid Move Handling...")
    result = client.submit_move('invalid_move')
    print(f"   Invalid move result: {'❌ Properly rejected' if not result else '⚠️ Unexpected acceptance'}")
    
    print("\n🎉 Demo completed successfully!")
    print(f"\nTo continue with tournament:")
    print(f"1. Register {8 - len(state.get('players', []) if state else [])} more players")
    print(f"2. Use: python main.py play  (for interactive)")
    print(f"3. Use: python main.py auto 'BotName'  (for automated)")


if __name__ == '__main__':
    demo_client_features()