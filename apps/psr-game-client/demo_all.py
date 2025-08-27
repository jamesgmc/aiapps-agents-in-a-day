"""
demo_all.py
This script invokes demo.py and creates 4 players for the PSR game client demo.
"""

import subprocess
import sys
import threading

# Function to run demo.py with a given player name
def run_demo(player_name):
    print(f"\n--- Running demo.py for player: {player_name} ---")
    process = subprocess.Popen(
        [sys.executable, "demo.py", player_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    # Print stdout in real time
    def stream_output(stream, is_stderr=False):
        for line in iter(stream.readline, ''):
            if is_stderr:
                sys.stderr.write(line)
                sys.stderr.flush()
            else:
                sys.stdout.write(line)
                sys.stdout.flush()
        stream.close()

    stdout_thread = threading.Thread(target=stream_output, args=(process.stdout, False))
    stderr_thread = threading.Thread(target=stream_output, args=(process.stderr, True))
    stdout_thread.start()
    stderr_thread.start()
    stdout_thread.join()
    stderr_thread.join()
    process.wait()

if __name__ == "__main__":
    player_names = ["Alice", "Bob", "Charlie", "Diana"]
    threads = []
    for name in player_names:
        t = threading.Thread(target=run_demo, args=(name,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
