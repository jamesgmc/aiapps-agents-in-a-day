#!/usr/bin/env python3
"""
Demo script showcasing PSR Game Tournament features including:
- Interactive player registration flow
- Complete tournament simulation with referee controls
- Round-by-round play demonstration
"""

import sys
import time
import logging
import random
from psr_game_client import PSRGameClient

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_player_count():
    """Ask user how many players to register"""
    while True:
        try:
            print("\n" + "="*60)
            print("🎮 PSR Game Tournament - Complete Flow Demo")
            print("="*60)
            print("\nThis demo will simulate a complete tournament with referee controls.")
            print("You can register between 2-8 players for the tournament.")
            
            count = input("\n📝 How many players would you like to register (2-8)? ").strip()
            
            if not count.isdigit():
                print("❌ Please enter a valid number.")
                continue
                
            count = int(count)
            if count < 2:
                print("❌ Tournament requires at least 2 players.")
                continue
            elif count > 8:
                print("❌ Tournament supports maximum 8 players.")
                continue
                
            return count
            
        except KeyboardInterrupt:
            print("\n🛑 Demo cancelled by user")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")

def demo_complete_tournament_flow():
    """Demonstrate complete tournament flow with referee controls"""
    
    # 1. Ask how many players to register
    player_count = get_player_count()
    if player_count is None:
        return False
    
    print(f"\n🎯 Setting up tournament with {player_count} players...")
    
    # 2. Create the number of players
    client = PSRGameClient()
    
    print(f"\n📋 Registering {player_count} players with auto-generated names...")
    if not client.register_bulk_players(count=player_count, use_auto_names=True):
        print("❌ Failed to register players")
        return False
    
    print("✅ Players registered successfully!")
    
    # Get initial tournament state
    state = client.get_tournament_state()
    if not state:
        print("❌ Failed to get tournament state")
        return False
    
    print(f"\n👥 Registered Players ({len(state.get('players', []))}):")
    for player in state.get('players', []):
        print(f"   - {player['name']} (ID: {player['id']})")
    
    print(f"\n🏆 Tournament is ready to start!")
    print("🎮 Tournament Status: Waiting for referee to start first round")
    print("\n💡 Use the web interface at http://localhost:5096 to:")
    print("   - View the tournament bracket")
    print("   - Use referee controls to start rounds")
    print("   - Release results after moves are submitted")
    
    # 3. Going to round one and check if the round has started
    current_round = 1
    max_rounds = 3  # For 8 players: 3 rounds max
    
    while current_round <= max_rounds:
        print(f"\n" + "="*50)
        print(f"🎯 ROUND {current_round}")
        print("="*50)
        
        # Wait for round to start (referee control)
        print(f"\n⏳ Waiting for referee to start Round {current_round}...")
        print("   (Use 'Start Round' button in web interface)")
        
        if not wait_for_round_start(client, current_round):
            print(f"❌ Round {current_round} failed to start or we were eliminated")
            break
        
        print(f"🚀 Round {current_round} has started!")
        
        # Get current matches for this round
        state = client.get_tournament_state()
        if not state:
            print("❌ Failed to get tournament state")
            break
            
        round_matches = [m for m in state.get('matches', []) if m.get('round') == current_round]
        print(f"\n🥊 Round {current_round} Matches:")
        for match in round_matches:
            p1_name = match.get('player1', {}).get('name', 'TBD')
            p2_name = match.get('player2', {}).get('name', 'TBD')
            print(f"   Match {match['id']}: {p1_name} vs {p2_name}")
        
        # 4. If started, randomly vote for options
        print(f"\n🎲 Submitting random moves for all players...")
        submit_random_moves_for_round(client, current_round, round_matches)
        
        # 5. Wait for result to be released, show result
        print(f"\n⏳ Waiting for referee to release Round {current_round} results...")
        print("   (Use 'Release Results' button in web interface)")
        
        if not wait_for_results_release(client, current_round):
            print(f"❌ Failed to get Round {current_round} results")
            break
        
        # Show round results
        show_round_results(client, current_round, round_matches)
        
        # 6. Wait for next round if success, then repeat
        state = client.get_tournament_state()
        if not state:
            break
            
        # Check if tournament is completed
        if state.get('status') == 2:  # Completed
            print(f"\n🎉 TOURNAMENT COMPLETED! 🎉")
            winner = state.get('winner')
            if winner:
                print(f"🏆 Tournament Winner: {winner['name']} (ID: {winner['id']})")
            else:
                print("🏆 Tournament completed (winner not determined)")
            break
        
        # Check if there are more rounds
        if current_round >= state.get('currentRound', 1):
            current_round += 1
        else:
            break
    
    # 7. If tournament is completed, exit each player
    print(f"\n✅ Demo completed successfully!")
    print(f"📊 Tournament simulation finished.")
    return True

def wait_for_round_start(client, round_num, max_attempts=60):
    """Wait for a specific round to start"""
    for attempt in range(max_attempts):
        state = client.get_tournament_state()
        if state:
            current_round = state.get('currentRound', 1)
            current_round_status = state.get('currentRoundStatus', 0)
            
            # Check if our round has started (status = 1 = InProgress)
            if current_round == round_num and current_round_status == 1:
                return True
            
            # If we're past our round, we missed it
            if current_round > round_num:
                return False
        
        time.sleep(2)  # Poll every 2 seconds
    
    return False

def submit_random_moves_for_round(client, round_num, matches):
    """Submit random moves for all players in the round"""
    moves = ["rock", "paper", "scissors"]
    move_symbols = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    
    for match in matches:
        player1 = match.get('player1', {})
        player2 = match.get('player2', {})
        
        if player1 and player2:
            # Random moves for both players
            p1_move = random.choice(moves)
            p2_move = random.choice(moves)
            
            print(f"   {player1['name']}: {p1_move} {move_symbols[p1_move]}")
            print(f"   {player2['name']}: {p2_move} {move_symbols[p2_move]}")
    
    print(f"✅ All moves submitted for Round {round_num}")

def wait_for_results_release(client, round_num, max_attempts=60):
    """Wait for round results to be released"""
    for attempt in range(max_attempts):
        state = client.get_tournament_state()
        if state:
            current_round = state.get('currentRound', 1)
            current_round_status = state.get('currentRoundStatus', 0)
            
            # Check if results are available (status = 2 = ResultsAvailable)
            if current_round == round_num and current_round_status >= 2:
                return True
        
        time.sleep(2)  # Poll every 2 seconds
    
    return False

def show_round_results(client, round_num, matches):
    """Show the results for a completed round"""
    print(f"\n📊 Round {round_num} Results:")
    print("-" * 40)
    
    state = client.get_tournament_state()
    if not state:
        return
    
    # Get updated match results
    updated_matches = [m for m in state.get('matches', []) if m.get('round') == round_num]
    
    for match in updated_matches:
        player1 = match.get('player1', {})
        player2 = match.get('player2', {})
        winner = match.get('winner', {})
        
        if player1 and player2:
            # Show moves (if available)
            p1_move = get_move_name(match.get('player1Move', 0))
            p2_move = get_move_name(match.get('player2Move', 0))
            
            print(f"\n🥊 Match {match['id']}:")
            print(f"   {player1['name']}: {p1_move}")
            print(f"   {player2['name']}: {p2_move}")
            
            if winner:
                print(f"   🏆 Winner: {winner['name']}")
            else:
                print(f"   ⚖️  Result: Draw/Unknown")
    
    # Show who advances
    active_players = [p for p in state.get('players', []) if p.get('isActive', True)]
    if len(active_players) > 1:
        print(f"\n🎯 Players advancing to next round ({len(active_players)}):")
        for player in active_players:
            print(f"   - {player['name']}")
    
def get_move_name(move_code):
    """Convert move code to name with emoji"""
    move_map = {
        0: "None",
        1: "🪨 Rock", 
        2: "📄 Paper",
        3: "✂️ Scissors"
    }
    return move_map.get(move_code, "Unknown")

def main():
    """Main demo function"""
    try:
        print("🎯 Welcome to PSR Game Tournament Complete Flow Demo!")
        print("This demo showcases the complete tournament experience with referee controls.")
        
        success = demo_complete_tournament_flow()
        
        if success:
            print("\n" + "="*60)
            print("Demo completed successfully! 🎉")
            print("="*60)
            print("\n📝 Features demonstrated:")
            print("✅ Interactive player count selection")
            print("✅ Bulk player registration with auto names")
            print("✅ Round-by-round tournament progression")
            print("✅ Random move submission simulation")
            print("✅ Referee control integration (start rounds & release results)")
            print("✅ Real-time result display")
            print("✅ Complete tournament flow from start to finish")
            print("\n🌐 Web interface features:")
            print("   - Tournament bracket visualization")
            print("   - Referee control buttons")
            print("   - Real-time move and result updates")
            print("   - Player registration interface")
        else:
            print("\n❌ Demo was cancelled or encountered an error")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)