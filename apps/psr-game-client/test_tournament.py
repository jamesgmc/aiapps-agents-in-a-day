#!/usr/bin/env python3
"""
Quick test script to register 8 players and test tournament flow
"""

import time
import subprocess
import threading
from psr_game_client import PSRGameClient


def register_and_play_bot(player_name):
    """Register and play as a bot"""
    client = PSRGameClient()
    
    if not client.register_player(player_name):
        print(f"Failed to register {player_name}")
        return
    
    print(f"✅ {player_name} registered (ID: {client.player_id})")
    
    # Play with random strategy
    from main import random_strategy
    success = client.play_tournament(strategy_func=random_strategy)
    print(f"🏁 {player_name} tournament result: {'Success' if success else 'Failed'}")


def main():
    print("🎮 Testing PSR Game Client with 8 players")
    print("==========================================")
    
    # Register 8 players in parallel
    player_names = [f"Bot{i}" for i in range(1, 9)]
    threads = []
    
    for name in player_names:
        thread = threading.Thread(target=register_and_play_bot, args=(name,))
        threads.append(thread)
        thread.start()
        time.sleep(0.5)  # Small delay between registrations
    
    # Wait for all to complete
    for thread in threads:
        thread.join()
    
    print("\n🏁 Test completed!")


if __name__ == '__main__':
    main()