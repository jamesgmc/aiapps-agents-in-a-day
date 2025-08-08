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
    
    # Demo 2: Auto Name Generation
    print("\n2️⃣ Testing Auto Name Generation...")
    auto_name = client.generate_auto_name()
    if auto_name:
        print(f"   Generated auto name: {auto_name}")
    else:
        print("   ❌ Auto name generation failed")
    
    # Demo 3: Player Registration (with choice)
    print("\n3️⃣ Registering Demo Player...")
    use_auto = input("   Use auto-generated name? (y/n): ").lower().startswith('y')
    
    if use_auto:
        if client.register_player(use_auto_name=True):
            print(f"   ✅ Successfully registered as '{client.player_name}'")
            print(f"   Player ID: {client.player_id}")
            print(f"   Tournament ID: {client.tournament_id}")
        else:
            print("   ❌ Registration failed")
            return
    else:
        player_name = f"DemoPlayer_{int(time.time())}"
        if client.register_player(player_name):
            print(f"   ✅ Successfully registered as '{player_name}'")
            print(f"   Player ID: {client.player_id}")
            print(f"   Tournament ID: {client.tournament_id}")
        else:
            print("   ❌ Registration failed")
            return
    
    # Demo 4: Updated Tournament Status
    print("\n4️⃣ Updated Tournament Status...")
    state = client.get_tournament_state()
    if state:
        print(f"   Players now: {len(state.get('players', []))}/8")
        print(f"   Round Status: {state.get('currentRoundStatus', 0)} (0=Waiting, 1=InProgress, 2=ResultsAvailable)")
        players_needed = 8 - len(state.get('players', []))
        if players_needed > 0:
            print(f"   Waiting for {players_needed} more players to start tournament")
            
            # Demo 5: Bulk Registration Option
            print("\n5️⃣ Bulk Registration Option...")
            auto_fill = input(f"   Auto-register {players_needed} players to start tournament? (y/n): ").lower().startswith('y')
            if auto_fill:
                if client.register_bulk_players(count=players_needed, use_auto_names=True):
                    print(f"   ✅ Successfully registered {players_needed} auto players")
                    print("   Tournament should start automatically!")
                    time.sleep(2)  # Wait for tournament to start
                    state = client.get_tournament_state()
                    if state:
                        status_names = ['WaitingForPlayers', 'InProgress', 'Completed']
                        print(f"   Updated Status: {status_names[state.get('status', 0)]}")
                else:
                    print("   ❌ Bulk registration failed")
        else:
            print("   Tournament ready to start!")
    
    # Demo 6: Current Match Check
    print("\n6️⃣ Checking for Current Match...")
    match = client.get_current_match()
    if match:
        print(f"   Active match found: Round {match.get('round')}")
        print(f"   Match ID: {match.get('id')}")
        opponent = match.get('player2') if match.get('player1', {}).get('id') == client.player_id else match.get('player1')
        if opponent:
            print(f"   Opponent: {opponent.get('name')}")
    else:
        print("   No active match (expected - tournament not started)")
    
    # Demo 7: Move Validation
    print("\n7️⃣ Testing Move Validation...")
    valid_moves = ['rock', 'paper', 'scissors']
    test_move = random.choice(valid_moves)
    print(f"   Testing move: {test_move}")
    result = client.submit_move(test_move)
    if result:
        print("   ✅ Move accepted")
    else:
        print("   ❌ Move rejected (expected if no active match or round not started)")
    
    # Demo 8: Invalid move test
    print("\n8️⃣ Testing Invalid Move Handling...")
    result = client.submit_move('invalid_move')
    print(f"   Invalid move result: {'❌ Properly rejected' if not result else '⚠️ Unexpected acceptance'}")
    
    print("\n🎉 Demo completed successfully!")
    print(f"\nNext steps:")
    print(f"1. Open web interface: http://localhost:5096")
    print(f"2. Use referee controls to start rounds and release results")
    print(f"3. For interactive play: python main.py play")
    print(f"4. For automated play: python main.py auto 'BotName'")
    print(f"5. For feature demo: python demo_features.py")


if __name__ == '__main__':
    demo_client_features()