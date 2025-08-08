#!/usr/bin/env python3
"""
PSR Game Client - Main CLI Interface
"""

import argparse
import logging
import sys
import random
from typing import Optional, Dict, Any

from psr_game_client import PSRGameClient
from config import DEFAULT_SERVER_URL, MOVES


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' if verbose else '%(levelname)s: %(message)s'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def random_strategy(round_num: int, match_info: Dict[str, Any]) -> str:
    """Random move strategy for automated play"""
    moves = list(MOVES.keys())
    choice = random.choice(moves)
    print(f"  [AUTO] Choosing {choice.capitalize()} for round {round_num}")
    return choice


def interactive_mode(client: PSRGameClient) -> None:
    """Run client in interactive mode"""
    print("\n🎮 PSR Game Client - Interactive Mode")
    print("=====================================")
    
    # Get player name
    name = input("Enter your player name: ").strip()
    if not name:
        print("Error: Player name cannot be empty")
        return
    
    # Register player
    if not client.register_player(name):
        print("Failed to register player")
        return
    
    print(f"\n✅ Successfully registered as '{name}' (ID: {client.player_id})")
    
    # Play tournament
    success = client.play_tournament()
    
    if success:
        print("\n🏁 Tournament completed!")
    else:
        print("\n❌ Tournament ended early")


def auto_mode(client: PSRGameClient, player_name: str) -> None:
    """Run client in automated mode"""
    print(f"\n🤖 PSR Game Client - Auto Mode (Player: {player_name})")
    print("====================================================")
    
    # Register player
    if not client.register_player(player_name):
        print("Failed to register player")
        return
    
    print(f"✅ Successfully registered as '{player_name}' (ID: {client.player_id})")
    
    # Play tournament with random strategy
    success = client.play_tournament(strategy_func=random_strategy)
    
    if success:
        print("🏁 Tournament completed!")
    else:
        print("❌ Tournament ended early")


def status_mode(client: PSRGameClient) -> None:
    """Show tournament status"""
    print("\n📊 Tournament Status")
    print("===================")
    
    state = client.get_tournament_state()
    if not state:
        print("❌ Could not retrieve tournament state")
        return
    
    print(f"Tournament ID: {state.get('tournamentId', 'Unknown')}")
    print(f"Tournament Name: {state.get('tournamentName', 'Unknown')}")
    print(f"Status: {['WaitingForPlayers', 'InProgress', 'Completed'][state.get('status', 0)]}")
    print(f"Current Round: {state.get('currentRound', 1)}")
    print(f"Players: {len(state.get('players', []))}")
    
    # Show players
    players = state.get('players', [])
    if players:
        print("\nRegistered Players:")
        for i, player in enumerate(players, 1):
            status = "Active" if player.get('isActive', True) else "Eliminated"
            print(f"  {i}. {player.get('name', 'Unknown')} (ID: {player.get('id', 'Unknown')}) - {status}")
    
    # Show matches
    matches = state.get('matches', [])
    if matches:
        print(f"\nMatches ({len(matches)} total):")
        for match in matches:
            round_num = match.get('round', 1)
            status = ['Pending', 'InProgress', 'Completed'][match.get('status', 0)]
            p1_name = match.get('player1', {}).get('name', 'TBD') if match.get('player1') else 'TBD'
            p2_name = match.get('player2', {}).get('name', 'TBD') if match.get('player2') else 'TBD'
            winner_name = match.get('winner', {}).get('name', 'TBD') if match.get('winner') else 'TBD'
            
            print(f"  Round {round_num}: {p1_name} vs {p2_name} - {status}")
            if status == 'Completed':
                print(f"    Winner: {winner_name}")
    
    # Show tournament winner
    if state.get('status') == 2:  # Completed
        winner = state.get('winner')
        if winner:
            print(f"\n🏆 Tournament Winner: {winner.get('name', 'Unknown')} (ID: {winner.get('id', 'Unknown')})")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='PSR Game Client')
    parser.add_argument('--server', '-s', default=DEFAULT_SERVER_URL, 
                       help=f'Server URL (default: {DEFAULT_SERVER_URL})')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Interactive mode
    interactive_parser = subparsers.add_parser('play', help='Play tournament interactively')
    
    # Auto mode
    auto_parser = subparsers.add_parser('auto', help='Play tournament automatically')
    auto_parser.add_argument('name', help='Player name for auto mode')
    
    # Status mode
    status_parser = subparsers.add_parser('status', help='Show tournament status')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Create client
    client = PSRGameClient(args.server)
    
    # Execute command
    if args.command == 'play':
        interactive_mode(client)
    elif args.command == 'auto':
        auto_mode(client, args.name)
    elif args.command == 'status':
        status_mode(client)
    else:
        # No command specified, show help
        parser.print_help()
        print("\nExamples:")
        print("  python main.py play                    # Interactive mode")
        print("  python main.py auto 'Bot Player'       # Automated mode")
        print("  python main.py status                  # Show tournament status")
        print("  python main.py --server http://localhost:5096 play")


if __name__ == '__main__':
    main()