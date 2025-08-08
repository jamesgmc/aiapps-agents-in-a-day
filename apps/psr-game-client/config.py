"""
Configuration settings for PSR Game Client
"""

# Server settings
DEFAULT_SERVER_URL = "http://localhost:5096"
DEFAULT_API_BASE = "/api"

# Polling settings
POLL_INTERVAL_SECONDS = 2  # How often to check tournament state
MAX_POLL_ATTEMPTS = 300   # Maximum polling attempts (10 minutes at 2s intervals)

# Game settings
MOVES = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}

MOVE_NAMES = {
    1: "Rock",
    2: "Paper", 
    3: "Scissors"
}

# Tournament settings
REQUIRED_PLAYERS = 8  # Tournament starts when this many players register