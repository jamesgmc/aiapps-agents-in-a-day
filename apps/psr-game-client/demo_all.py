"""
demo_all.py
This script invokes demo.py and creates 4 players for the PSR game client demo.
"""
import subprocess
import sys

# Function to run demo.py with a given player name
def run_demo(player_name):
    print(f"\n--- Running demo.py for player: {player_name} ---")
    result = subprocess.run([sys.executable, "demo.py", player_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

if __name__ == "__main__":
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    for name in player_names:
        run_demo(name)
