import requests
import json
from typing import Optional, Dict, Any

class PSRGameClient:
    """Client for communicating with the PSR Game Server API"""
    
    def __init__(self, base_url: str = "http://localhost:5289"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def register_player(self, name: str) -> Dict[str, Any]:
        """Register a new player with the server"""
        url = f"{self.base_url}/api/player/register"
        data = {"Name": name}
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def get_player_status(self, player_id: int) -> Dict[str, Any]:
        """Get current tournament status for a player"""
        url = f"{self.base_url}/api/player/{player_id}/status"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def submit_answer(self, player_id: int, round_number: int, answer: str, move: int) -> Dict[str, Any]:
        """Submit answer and RPS move for current round"""
        url = f"{self.base_url}/api/player/submit-answer"
        data = {
            "PlayerId": player_id,
            "RoundNumber": round_number,
            "Answer": answer,
            "Move": move  # 0=Rock, 1=Paper, 2=Scissors
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def get_player_results(self, player_id: int) -> Dict[str, Any]:
        """Get all results for a specific player"""
        url = f"{self.base_url}/api/player/{player_id}/results"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}