"""
Example usage of GameAgentV1 with the RPS Game Server API
This demonstrates how to integrate the Azure AI Agent with the tournament system.
"""

import sys
import os
import time
import requests
from agent_v1 import GameAgentV1

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class RPSGameClient:
    """Client for interacting with RPS Game Server using Azure AI Agent V1"""
    
    def __init__(self, server_url: str = "http://localhost:5289", player_name: str = "AI_Agent_V1"):
        self.server_url = server_url.rstrip('/')
        self.player_name = player_name
        self.player_id = None
        self.agent = GameAgentV1()
        
    def register_player(self) -> bool:
        """Register the agent as a player in the tournament"""
        try:
            response = requests.post(
                f"{self.server_url}/api/player/register",
                json={"Name": self.player_name},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.player_id = data.get('playerId')
                print(f"✅ Registered as player: {self.player_name} (ID: {self.player_id})")
                return True
            else:
                print(f"❌ Registration failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Registration error: {str(e)}")
            return False
    
    def get_player_status(self) -> dict:
        """Get current player status and tournament information"""
        if not self.player_id:
            return {}
            
        try:
            response = requests.get(f"{self.server_url}/api/player/{self.player_id}/status", timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"❌ Error getting player status: {str(e)}")
            return {}
    
    def submit_answer_and_move(self, round_number: int, answer: str, move: int) -> bool:
        """Submit answer and RPS move for the current round"""
        try:
            payload = {
                "PlayerId": self.player_id,
                "RoundNumber": round_number,
                "Answer": answer,
                "Move": move
            }
            
            response = requests.post(
                f"{self.server_url}/api/player/submit-answer",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Submitted answer: '{answer}' and move: {self.agent.get_move_name(move)}")
                return True
            else:
                print(f"❌ Submission failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Submission error: {str(e)}")
            return False
    
    def play_tournament(self):
        """Main game loop for participating in the tournament"""
        print(f"🚀 Starting RPS Tournament Client with Azure AI Agent V1")
        print(f"🎯 Agent using: {'Azure AI Service' if self.agent.use_azure_ai else 'Local Processing'}")
        print("=" * 60)
        
        # Register player
        if not self.register_player():
            return
        
        # Monitor and participate in the tournament
        print("⏳ Monitoring tournament status...")
        
        while True:
            try:
                # Get current player status
                status = self.get_player_status()
                
                if not status or 'error' in status:
                    print("❌ Could not get player status")
                    time.sleep(5)
                    continue
                
                tournament_status = status.get('tournamentStatus', 'Unknown')
                current_round = status.get('currentRound', 0)
                round_status = status.get('roundStatus', 'Unknown')
                question = status.get('question', '')
                
                print(f"📊 Tournament: {tournament_status}, Round: {current_round}, Status: {round_status}")
                
                # Check if tournament is completed
                if tournament_status == 'Completed':
                    print("🏁 Tournament completed!")
                    self.show_final_results()
                    break
                
                # Check if we can participate in current round
                if (tournament_status == 'InProgress' and 
                    round_status == 'InProgress' and 
                    question and 
                    not status.get('hasSubmitted', False)):
                    
                    print(f"\n🎯 Playing Round {current_round}")
                    print(f"❓ Question: {question}")
                    
                    # Use Azure AI Agent to answer question
                    answer = self.agent.answer_question(question)
                    print(f"🤖 AI Answer: {answer}")
                    
                    # Choose RPS move
                    move = self.agent.choose_rps_move()
                    move_name = self.agent.get_move_name(move)
                    print(f"✊ RPS Move: {move_name}")
                    
                    # Submit answer and move
                    self.submit_answer_and_move(current_round, answer, move)
                
                elif status.get('hasSubmitted', False):
                    print(f"✅ Already submitted for round {current_round}, waiting...")
                
                # Wait before checking again
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping tournament participation...")
                break
            except Exception as e:
                print(f"❌ Error in tournament loop: {str(e)}")
                time.sleep(5)
    
    def show_final_results(self):
        """Show final tournament results"""
        try:
            response = requests.get(f"{self.server_url}/api/player/{self.player_id}/results", timeout=10)
            if response.status_code == 200:
                results = response.json()
                print("\n🏆 Your Tournament Results:")
                print("-" * 40)
                
                total_score = 0
                for result in results:
                    round_num = result.get('roundNumber', 0)
                    score = result.get('score', 0)
                    answer = result.get('answer', '')
                    move = result.get('move', 0)
                    move_name = self.agent.get_move_name(move)
                    
                    total_score += score
                    print(f"Round {round_num}: {score} points (Answer: '{answer}', Move: {move_name})")
                
                print(f"\n� Total Score: {total_score} points")
                
        except Exception as e:
            print(f"❌ Error getting final results: {str(e)}")


def main():
    """Main function to run the RPS game client"""
    # You can customize these parameters
    server_url = "http://localhost:5289"  # Updated to match actual server port
    player_name = "Azure_AI_Agent_V1"
    
    # Create and run the game client
    client = RPSGameClient(server_url, player_name)
    try:
        client.play_tournament()
    except KeyboardInterrupt:
        print("\n\n⏹️  Game client stopped by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
