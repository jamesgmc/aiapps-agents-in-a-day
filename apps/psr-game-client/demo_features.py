#!/usr/bin/env python3
"""
Demo script showcasing PSR Game Tournament features including:
- Auto player name generation
- Bulk player registration for simulation
- Auto-play strategy
"""

import sys
import time
import logging
from psr_game_client import PSRGameClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def demo_auto_features():
    """Demonstrate auto player features"""
    print("\n" + "="*60)
    print("🎮 PSR Game Tournament - Auto Features Demo")
    print("="*60)
    
    client = PSRGameClient()
    
    print("\n1. Auto Player Name Generation:")
    print("-" * 30)
    for i in range(5):
        name = client.generate_auto_name()
        print(f"   Generated name {i+1}: {name}")
    
    print("\n2. Single Player Registration with Auto Name:")
    print("-" * 50)
    if client.register_player(use_auto_name=True):
        print(f"   ✅ Registered as: {client.player_name}")
        print(f"   Player ID: {client.player_id}")
        print(f"   Tournament ID: {client.tournament_id}")
    
    print("\n3. Tournament State Before Full Registration:")
    print("-" * 50)
    state = client.get_tournament_state()
    if state:
        print(f"   Players: {len(state.get('players', []))}/8")
        print(f"   Status: {state.get('status')} (0=Waiting, 1=InProgress, 2=Completed)")
        print(f"   Round: {state.get('currentRound')}")
        print(f"   Round Status: {state.get('currentRoundStatus')} (0=Waiting, 1=InProgress, 2=ResultsAvailable, 3=Completed)")
    
    print("\n4. Bulk Registration for Simulation:")
    print("-" * 40)
    remaining_players = 8 - len(state.get('players', [])) if state else 7
    if remaining_players > 0:
        print(f"   Registering {remaining_players} auto players...")
        if client.register_bulk_players(count=remaining_players, use_auto_names=True):
            print("   ✅ Bulk registration successful!")
        else:
            print("   ❌ Bulk registration failed")
    
    print("\n5. Final Tournament State:")
    print("-" * 30)
    time.sleep(2)  # Wait for tournament to start
    state = client.get_tournament_state()
    if state:
        print(f"   Players: {len(state.get('players', []))}/8")
        print(f"   Status: {state.get('status')} (0=Waiting, 1=InProgress, 2=Completed)")
        print(f"   Round: {state.get('currentRound')}")
        print(f"   Round Status: {state.get('currentRoundStatus')}")
        
        print("\n   Registered Players:")
        for player in state.get('players', []):
            marker = " 👤 (You)" if player['id'] == client.player_id else ""
            print(f"     - {player['name']} (ID: {player['id']}){marker}")
        
        if state.get('matches'):
            print(f"\n   Matches Created: {len(state.get('matches'))}")
            for match in state.get('matches'):
                p1_name = match.get('player1', {}).get('name', 'TBD')
                p2_name = match.get('player2', {}).get('name', 'TBD')
                print(f"     Round {match['round']}: {p1_name} vs {p2_name}")

def demo_auto_play():
    """Demonstrate auto-play functionality"""
    print("\n" + "="*60)
    print("🤖 Auto-Play Strategy Demo")
    print("="*60)
    
    client = PSRGameClient()
    
    # Register and play with auto strategy
    if client.register_player(use_auto_name=True):
        print(f"\n🎮 Playing as: {client.player_name}")
        
        # Wait for tournament to have enough players
        print("\n⏳ Waiting for tournament to start...")
        if client.wait_for_tournament_start():
            print("🚀 Tournament started!")
            
            # Play tournament with auto strategy
            print("\n🤖 Playing tournament with auto strategy...")
            try:
                result = client.play_tournament(strategy_func=client.auto_play_strategy)
                if result:
                    print("✅ Tournament completed successfully!")
                else:
                    print("⚠️ Tournament ended (eliminated or error)")
            except KeyboardInterrupt:
                print("\n🛑 Demo interrupted by user")
        else:
            print("❌ Tournament failed to start")
    else:
        print("❌ Failed to register player")

def main():
    """Main demo function"""
    try:
        print("🎯 Welcome to PSR Game Tournament Feature Demo!")
        print("This demo showcases the new auto-player and simulation features.")
        
        demo_auto_features()
        
        print("\n" + "="*60)
        print("Demo completed! 🎉")
        print("="*60)
        print("\n📝 Features demonstrated:")
        print("✅ Auto player name generation")
        print("✅ Single player registration with auto names")
        print("✅ Bulk player registration for simulation")
        print("✅ Tournament state monitoring")
        print("✅ Round status tracking")
        print("\n🌐 Check the web interface at: http://localhost:5096")
        print("   - Use referee controls to start rounds and release results")
        print("   - View real-time tournament bracket")
        print("   - See player moves (hidden until results are released)")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)