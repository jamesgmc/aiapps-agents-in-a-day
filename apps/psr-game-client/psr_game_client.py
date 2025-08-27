"""
PSR Game Client - Paper Scissors Rock tournament client
"""

import requests
import time
import logging
from typing import Optional, Dict, Any
from config import (
    DEFAULT_SERVER_URL, DEFAULT_API_BASE, POLL_INTERVAL_SECONDS, 
    MAX_POLL_ATTEMPTS, MOVES, MOVE_NAMES
)


class PSRGameClient:
    """Client for interacting with PSR Game Server API"""
    
    def __init__(self, server_url: str = DEFAULT_SERVER_URL):
        self.server_url = server_url.rstrip('/')
        self.api_base = DEFAULT_API_BASE
        self.base_url = f"{self.server_url}{self.api_base}"
        self.player_id: Optional[int] = None
        self.player_name: Optional[str] = None
        self.tournament_id: Optional[int] = None
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def register_player(self, name: str = None, use_auto_name: bool = False) -> bool:
        """
        Register a new player for the tournament
        
        Args:
            name: Player name (optional if use_auto_name is True)
            use_auto_name: If True, get an auto-generated name from server
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        if use_auto_name and not name:
            # Get auto-generated name from server
            name = self.generate_auto_name()
            if not name:
                self.logger.error("Failed to generate auto name")
                return False
        
        if not name:
            self.logger.error("Player name is required")
            return False
            
        url = f"{self.base_url}/players/register"
        payload = {"name": name}
        
        try:
            self.logger.info(f"Registering player: {name}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            self.player_id = data["playerId"]
            self.player_name = data["playerName"]
            self.tournament_id = data["tournamentId"]
            
            self.logger.info(f"Successfully registered! Player ID: {self.player_id}, Tournament ID: {self.tournament_id}")
            self.logger.info(f"Message: {data.get('message', '')}")
            
            return True
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to register player: {e}")
            return False
    
    def generate_auto_name(self) -> Optional[str]:
        """
        Generate an auto player name from the server
        
        Returns:
            str: Generated name or None if error
        """
        url = f"{self.base_url}/players/generate-name"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("name")
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to generate auto name: {e}")
            return None
    
    def register_bulk_players(self, count: int, use_auto_names: bool = True, names: list = None) -> bool:
        """
        Register multiple players for simulation
        
        Args:
            count: Number of players to register
            use_auto_names: Whether to use auto-generated names
            names: List of custom names (if not using auto names)
            
        Returns:
            bool: True if registration successful, False otherwise
        """
        url = f"{self.base_url}/players/register-bulk"
        payload = {
            "count": count,
            "useAutoNames": use_auto_names,
            "names": names or []
        }
        
        try:
            self.logger.info(f"Registering {count} players (auto names: {use_auto_names})")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info(f"Successfully registered {len(data['players'])} players")
            self.logger.info(f"Message: {data.get('message', '')}")
            
            return True
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to register bulk players: {e}")
            return False
    
    def get_tournament_state(self) -> Optional[Dict[str, Any]]:
        """
        Get the current tournament state
        
        Returns:
            Dict containing tournament state or None if error
        """
        url = f"{self.base_url}/tournament/state"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to get tournament state: {e}")
            return None
    
    def get_current_match(self) -> Optional[Dict[str, Any]]:
        """
        Get current match for this player
        
        Returns:
            Dict containing match info or None if no match/error
        """
        if not self.player_id:
            self.logger.error("Cannot get current match - player not registered")
            return None
            
        url = f"{self.base_url}/players/{self.player_id}/current-match"
        self.logger.info(f"get_current_match={url}")
        
        try:
            response = requests.get(url)
            if response.status_code == 404:
                return None  # No active match
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to get current match: {e}")
            return None
        
        
    def get_current_match_completed(self) -> Optional[Dict[str, Any]]:
        """
        Get current match for this player
        
        Returns:
            Dict containing match info or None if no match/error
        """
        if not self.player_id:
            self.logger.error("Cannot get current match - player not registered")
            return None
            
        url = f"{self.base_url}/players/{self.player_id}/current-match-completed"
        self.logger.info(f"get_current_match_completed={url}")
        
        try:
            response = requests.get(url)
            if response.status_code == 404:
                return None  # No active match
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to get current match: {e}")
            return None
    
    def submit_move(self, move: str) -> bool:
        """
        Submit a move for the current match
        
        Args:
            move: Move name ("rock", "paper", "scissors")
            
        Returns:
            bool: True if move submitted successfully, False otherwise
        """
        if not self.player_id:
            self.logger.error("Cannot submit move - player not registered")
            return False
            
        if move.lower() not in MOVES:
            self.logger.error(f"Invalid move: {move}. Must be one of: {list(MOVES.keys())}")
            return False
        
        url = f"{self.base_url}/players/{self.player_id}/move"
        payload = {"move": MOVES[move.lower()]}
        
        try:
            self.logger.info(f"Submitting move: {move}")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            data = response.json()
            if data.get("success", False):
                self.logger.info("Move submitted successfully!")
                self.logger.info(f"Message: {data.get('message', '')}")
                return True
            else:
                self.logger.warning(f"Move submission failed: {data.get('message', '')}")
                return False
                
        except requests.RequestException as e:
            self.logger.error(f"Failed to submit move: {e}")
            return False
    
    def wait_for_tournament_start(self) -> bool:
        """
        Wait for tournament to start (when enough players register)
        
        Returns:
            bool: True if tournament started, False if timeout
        """
        self.logger.info("Waiting for tournament to start...")
        
        for attempt in range(MAX_POLL_ATTEMPTS):
            state = self.get_tournament_state()
            if state and state.get("status") != 0:  # 0 = WaitingForPlayers
                self.logger.info("Tournament has started!")
                return True
                
            self.logger.info(f"Tournament status: WaitingForPlayers. Players registered: {len(state.get('players', [])) if state else 'Unknown'}")
            time.sleep(POLL_INTERVAL_SECONDS)
        
        self.logger.error("Timeout waiting for tournament to start")
        return False
    
    def wait_for_round_to_start(self, expected_round: int) -> bool:
        """
        Wait for a specific round to start (round status = InProgress)
        
        Args:
            expected_round: The round number to wait for
            
        Returns:
            bool: True if round started, False if timeout or eliminated
        """
        self.logger.info(f"Waiting for round {expected_round} to start...")
        
        for attempt in range(MAX_POLL_ATTEMPTS):
            # Check tournament state to see current round status
            state = self.get_tournament_state()
            if state:
                current_round = state.get("currentRound", 1)
                current_round_status = state.get("currentRoundStatus", 0)
                players = state.get("players", [])
                
                # Check if we're still an active player
                our_player = next((p for p in players if p["id"] == self.player_id), None)
                if not our_player or not our_player.get("isActive", True):
                    self.logger.info("Player has been eliminated from tournament")
                    return False
                
                # If current round is higher than expected, we missed our round
                if current_round > expected_round:
                    self.logger.warning(f"Missed round {expected_round}, tournament is now on round {current_round}")
                    return False
                
                # Check if our expected round is in progress (status = 1)
                if current_round == expected_round and current_round_status == 1:
                    # Also check if we have an active match
                    match = self.get_current_match()
                    if match and match.get("round") == expected_round and match.get("status") == 1:  # 1 = InProgress
                        self.logger.info(f"Round {expected_round} has started!")
                        return True
                
                self.logger.info(f"Current round: {current_round} (status: {current_round_status}), waiting for round {expected_round}")
            
            time.sleep(POLL_INTERVAL_SECONDS)
        
        self.logger.error(f"Timeout waiting for round {expected_round} to start")
        return False
    
    def play_tournament(self, strategy_func=None) -> bool:
        """
        Play through the entire tournament
        
        Args:
            strategy_func: Function that returns move choice, defaults to asking user
            
        Returns:
            bool: True if completed tournament, False if error/eliminated
        """
        if not self.player_id:
            self.logger.error("Cannot play tournament - player not registered")
            return False
        
        # Wait for tournament to start
        if not self.wait_for_tournament_start():
            return False
        
        current_round = 1
        
        while True:
            # Wait for our round to start
            if not self.wait_for_round_to_start(current_round):
                # Either eliminated or error
                return False
            
            # Get our current match
            match = self.get_current_match()
            if not match:
                self.logger.error("No active match found")
                return False
            
            self.logger.info(f"Playing Round {current_round}")
            self.logger.info(f"Match ID: {match['id']}")
            
            # Show opponent info
            player1 = match.get("player1")
            player2 = match.get("player2")
            opponent = player2 if player1 and player1["id"] == self.player_id else player1
            
            if opponent:
                self.logger.info(f"Opponent: {opponent['name']} (ID: {opponent['id']})")
            
            # Get move choice
            if strategy_func:
                move = strategy_func(current_round, match)
            else:
                move = self._get_move_from_user()
            
            if not move:
                self.logger.error("No move selected")
                return False
            
            # Submit move
            if not self.submit_move(move):
                self.logger.error("Failed to submit move")
                return False
            
            # Wait for match to complete
            if not self._wait_for_match_completion(match["id"]):
                return False
         
            # Check if tournament is complete
            state = self.get_tournament_state()
            if state and state.get("status") == 2:  # 2 = Completed
                tournament_winner = state.get("winner")
                if tournament_winner and tournament_winner["id"] == self.player_id:
                    self.logger.info("🎉 WON THE TOURNAMENT! 🎉")
                else:
                    self.logger.info("Tournament completed.")
                return True
            
            current_round += 1
    
    def _get_move_from_user(self) -> Optional[str]:
        """Get move choice from user input"""
        while True:
            try:
                print("\nChoose your move:")
                print("1. Rock")
                print("2. Paper") 
                print("3. Scissors")
                choice = input("Enter your choice (1-3 or rock/paper/scissors): ").strip().lower()
                
                if choice in ["1", "rock"]:
                    return "rock"
                elif choice in ["2", "paper"]:
                    return "paper"
                elif choice in ["3", "scissors"]:
                    return "scissors"
                else:
                    print("Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nGame cancelled by user")
                return None
            except Exception as e:
                print(f"Error getting input: {e}")
                return None
    
    def _wait_for_match_completion(self, match_id: int) -> bool:
        """Wait for match to complete"""
        self.logger.info(f"Waiting for match to complete...match_id={match_id}")
        
        for attempt in range(MAX_POLL_ATTEMPTS):
            match = self.get_current_match_completed()
            self.logger.info(f"_wait_for_match_completion={match}")
            if match and match["id"] == match_id and match.get("status") == 2:  # 2 = Completed
                self.logger.info("Match completed!")
                
                # Show match results
                player1 = match.get("player1", {})
                player2 = match.get("player2", {})
                winner = match.get("winner", {})
                
                p1_move = MOVE_NAMES.get(match.get("player1Move", 0), "None")
                p2_move = MOVE_NAMES.get(match.get("player2Move", 0), "None")
                
                self.logger.info(f"Match Results:")
                self.logger.info(f"  {player1.get('name', 'Player1')}: {p1_move}")
                self.logger.info(f"  {player2.get('name', 'Player2')}: {p2_move}")
                self.logger.info(f"  Winner: {winner.get('name', 'Unknown')}")
                
                # Check if winner name matches player name
                winner_name = winner.get('name', '')
                if winner_name == self.player_name:
                    self.logger.info(f"Match Results: win")
                    return True
                else:
                    self.logger.info(f"Match Results: lost")
                    return False
            
            time.sleep(POLL_INTERVAL_SECONDS)
        
        self.logger.error("Timeout waiting for match completion")
        return False
    
    def auto_play_strategy(self, round_num: int, match: dict) -> str:
        """
        Simple auto-play strategy that randomly chooses moves
        
        Args:
            round_num: Current round number
            match: Match information
            
        Returns:
            str: Move choice ('rock', 'paper', or 'scissors')
        """
        import random
        moves = ["rock", "paper", "scissors"]
        choice = random.choice(moves)
        self.logger.info(f"Auto-play choosing: {choice}")
        return choice
    
    def simulate_tournament_participation(self, player_count: int = 8) -> bool:
        """
        Simulate tournament participation by registering multiple auto players
        
        Args:
            player_count: Number of players to register for simulation
            
        Returns:
            bool: True if simulation setup successful, False otherwise
        """
        if player_count > 8:
            self.logger.error("Maximum 8 players allowed per tournament")
            return False
        
        # Register bulk players with auto names
        if not self.register_bulk_players(player_count, use_auto_names=True):
            return False
        
        self.logger.info(f"Simulation started with {player_count} players")
        return True