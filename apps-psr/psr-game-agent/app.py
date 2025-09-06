from flask import Flask, render_template, request, jsonify, redirect, url_for
from agent import GameAgent
import threading

app = Flask(__name__)
game_agent = None

@app.route('/')
def index():
    """Main page - shows player name input or game status"""
    global game_agent
    
    if game_agent is None:
        # Show player name input form
        return render_template('index.html', show_form=True)
    else:
        # Show game status
        return render_template('index.html', 
                             show_form=False,
                             player_name=game_agent.player_name,
                             player_id=game_agent.player_id,
                             tournament_status=game_agent.tournament_status,
                             round_status=game_agent.round_status,
                             current_round=game_agent.current_round,
                             is_running=game_agent.is_running,
                             status_log=game_agent.status_log[-20:][::-1],  # Show last 20 messages, latest first
                             results=game_agent.results)

@app.route('/start', methods=['POST'])
def start_game():
    """Start the game with player name"""
    global game_agent
    
    player_name = request.form.get('player_name', '').strip()
    
    if not player_name:
        return redirect(url_for('index'))
    
    # Create new game agent
    game_agent = GameAgent(player_name)
    
    # Register player
    if game_agent.register_player():
        # Start autonomous play
        game_agent.start_autonomous_play()
        return redirect(url_for('index'))
    else:
        # Registration failed, reset
        game_agent = None
        return redirect(url_for('index'))

@app.route('/reconnect', methods=['POST'])
def reconnect_game():
    """Reconnect with existing player ID"""
    global game_agent
    
    player_id = request.form.get('player_id', '').strip()
    
    if not player_id:
        return redirect(url_for('index'))
    
    try:
        player_id = int(player_id)
    except ValueError:
        return redirect(url_for('index'))
    
    # Create game agent with existing player ID
    game_agent = GameAgent(f"Player {player_id}")
    game_agent.player_id = player_id
    
    # Verify the player exists by getting status
    from api_client import PSRGameClient
    client = PSRGameClient()
    status_response = client.get_player_status(player_id)
    
    if "error" in status_response:
        game_agent.log_status(f"Failed to reconnect: {status_response['error']}")
        game_agent = None
        return redirect(url_for('index'))
    
    game_agent.log_status(f"Successfully reconnected as Player ID: {player_id}")
    
    # Get current results
    game_agent.get_current_results()
    
    # Start autonomous play
    game_agent.start_autonomous_play()
    return redirect(url_for('index'))

@app.route('/reset')
def reset_game():
    """Reset the game to start over"""
    global game_agent
    
    if game_agent:
        game_agent.stop()
    
    game_agent = None
    return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    """API endpoint to get current game status"""
    global game_agent
    
    if game_agent is None:
        return jsonify({"status": "not_started"})
    
    return jsonify({
        "status": "running" if game_agent.is_running else "stopped",
        "player_name": game_agent.player_name,
        "player_id": game_agent.player_id,
        "tournament_status": game_agent.tournament_status,
        "round_status": game_agent.round_status,
        "current_round": game_agent.current_round,
        "recent_log": game_agent.status_log[-5:][::-1] if game_agent.status_log else [],  # Last 5 messages, latest first
        "results_count": len(game_agent.results)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)