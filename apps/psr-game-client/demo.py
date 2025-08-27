import sys
# Force UTF-8 encoding for stdout if not already set
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
else:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
 # Number of players required for the tournament
#!/usr/bin/env python3
"""
Demo script showing PSR Game Client functionality
"""

import time
import random
from psr_game_client import PSRGameClient

MAX_PLAYERS = 2 

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
    players = []  # Array to keep track of registered players
    
    # Demo 1: Tournament Status Check
    print("\n1️⃣ Checking Tournament Status...")
    state = client.get_tournament_state()
    if state:
        status_names = ['WaitingForPlayers', 'InProgress', 'Completed']
        print(f"   Tournament ID: {state.get('tournamentId')}")
        print(f"   Status: {status_names[state.get('status', 0)]}")
        print(f"   Players: {len(state.get('players', []))}/{MAX_PLAYERS}")
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
    
    if client.register_player(use_auto_name=True):
        print(f"   ✅ Successfully registered as '{client.player_name}'")
        print(f"   Player ID: {client.player_id}")
        print(f"   Tournament ID: {client.tournament_id}")
        players.append({'name': client.player_name, 'id': client.player_id})
    else:
        print("   ❌ Registration failed")
        return
    
    # Demo 4: Updated Tournament Status
    print("\n4️⃣ Updated Tournament Status...")
    state = client.get_tournament_state()
    if state:
        print(f"   Players now: {len(state.get('players', []))}/{MAX_PLAYERS}")
        print(f"   Round Status: {state.get('currentRoundStatus', 0)} (0=Waiting, 1=InProgress, 2=ResultsAvailable)")
        players_needed = MAX_PLAYERS - len(state.get('players', []))
        if players_needed > 0:
            print(f"   Waiting for {players_needed} more players to start tournament")
        else:
            print("   Tournament ready to start!")

    # Loop through the player array and print details
    if players:
        print("\n👥 Registered Players:")
        for idx, p in enumerate(players, 1):
            print(f"   {idx}. {p['name']} (ID: {p['id']})")
    
    # Demo 6: Current Match Check for all registered players
    print("\n6️⃣ Checking for Current Match for all registered players...")
    for p in players:
        # Temporarily set the client player_id to the player's id to check their match
        original_player_id = client.player_id
        original_player_name = client.player_name
        client.player_id = p['id']
        client.player_name = p['name']
        print(f"   Player: {p['name']} (ID: {p['id']})")
        while True:
            state = client.get_tournament_state()
            if not state or state.get('status', 0) == 2:  # 2 = Completed
                print("      Tournament completed or not found.")
                break
            match = client.get_current_match()
            if match:
                round_status = state.get('currentRoundStatus', 0)
                print(f"      Active match found: Round {match.get('round')}")
                print(f"      Match ID: {match.get('id')}")
                opponent = match.get('player2') if match.get('player1', {}).get('id') == client.player_id else match.get('player1')
                if opponent:
                    print(f"      Opponent: {opponent.get('name')}")
                # Wait for round to be InProgress (1)
                if round_status == 1:
                    # Submit move (vote)
                    move = random_move()
                    print(f"      Voting move: {move}")
                    client.submit_move(move)
                    # Wait for round to finish
                    while True:
                        state = client.get_tournament_state()
                        if state.get('currentRoundStatus', 0) != 1:
                            print("      Round finished. Checking for next round...")
                            break
                        time.sleep(1)
                else:
                    print("      Waiting for round to start...")
                    time.sleep(1)
            else:
                print("      No active match (expected - tournament not started or between rounds)")
                time.sleep(1)
        # Restore original client player_id and name
        client.player_id = original_player_id
        client.player_name = original_player_name
    
    
    print("\n🎉 Demo completed successfully!")
    print(f"\nNext steps:")
    print(f"1. Open web interface: http://localhost:5096")
    print(f"2. Use referee controls to start rounds and release results")
    print(f"3. For interactive play: python main.py play")
    print(f"4. For automated play: python main.py auto 'BotName'")
    print(f"5. For feature demo: python demo_features.py")


if __name__ == '__main__':
    demo_client_features()