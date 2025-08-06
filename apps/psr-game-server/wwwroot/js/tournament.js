// Tournament JavaScript Application
class TournamentApp {
    constructor() {
        this.currentTournament = null;
        this.currentPlayerId = null;
        this.signalRConnection = null;
        this.init();
    }

    async init() {
        // Initialize SignalR connection
        await this.initSignalR();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Load initial tournament state
        await this.loadTournamentState();
        
        // Start periodic updates
        this.startPeriodicUpdates();
    }

    async initSignalR() {
        try {
            this.signalRConnection = new signalR.HubConnectionBuilder()
                .withUrl("/gamehub")
                .build();

            this.signalRConnection.on("TournamentUpdate", (tournament) => {
                this.updateTournamentDisplay(tournament);
            });

            this.signalRConnection.on("MatchUpdate", (match) => {
                this.updateMatchDisplay(match);
            });

            await this.signalRConnection.start();
            console.log("SignalR connection established");
        } catch (error) {
            console.error("Error establishing SignalR connection:", error);
        }
    }

    setupEventListeners() {
        // Player registration form
        document.getElementById('register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.registerPlayer();
        });

        // Move buttons
        document.querySelectorAll('.move-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                await this.submitMove(parseInt(e.target.dataset.move));
            });
        });
    }

    async registerPlayer() {
        const nameInput = document.getElementById('player-name');
        const name = nameInput.value.trim();
        
        if (!name) {
            this.showMessage('Please enter a player name', 'danger');
            return;
        }

        try {
            const response = await fetch('/api/players/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name })
            });

            if (response.ok) {
                const result = await response.json();
                this.currentPlayerId = result.playerId;
                this.showMessage(result.message, 'success');
                nameInput.value = '';
                
                // Join tournament SignalR group
                if (this.signalRConnection && result.tournamentId) {
                    await this.signalRConnection.invoke("JoinTournament", result.tournamentId.toString());
                }
                
                await this.loadTournamentState();
            } else {
                const error = await response.json();
                this.showMessage(error.message || 'Registration failed', 'danger');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showMessage('Network error during registration', 'danger');
        }
    }

    async submitMove(move) {
        if (!this.currentPlayerId) {
            this.showMessage('Please register first', 'danger');
            return;
        }

        try {
            const response = await fetch(`/api/players/${this.currentPlayerId}/move`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ move })
            });

            if (response.ok) {
                const result = await response.json();
                this.showMessage(result.message, 'success');
                
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('moveModal'));
                if (modal) modal.hide();
                
                await this.loadTournamentState();
            } else {
                const error = await response.json();
                this.showMessage(error.message || 'Move submission failed', 'danger');
            }
        } catch (error) {
            console.error('Move submission error:', error);
            this.showMessage('Network error during move submission', 'danger');
        }
    }

    async loadTournamentState() {
        try {
            const response = await fetch('/api/tournament/state');
            
            if (response.ok) {
                const tournament = await response.json();
                this.currentTournament = tournament;
                this.updateTournamentDisplay(tournament);
            } else if (response.status === 404) {
                this.displayEmptyState();
            }
        } catch (error) {
            console.error('Error loading tournament state:', error);
        }
    }

    updateTournamentDisplay(tournament) {
        if (!tournament) return;

        // Update tournament info
        document.getElementById('tournament-title').textContent = tournament.tournamentName || 'Tournament';
        document.getElementById('player-count').textContent = `${tournament.players.length}/8`;
        document.getElementById('current-round').textContent = `Round ${tournament.currentRound}`;
        
        // Update status
        const statusElement = document.getElementById('tournament-status');
        const statusTextElement = document.getElementById('status-text');
        
        statusElement.className = 'badge ';
        switch (tournament.status) {
            case 0: // WaitingForPlayers
                statusElement.classList.add('bg-secondary');
                statusElement.textContent = 'Waiting for Players';
                statusTextElement.textContent = 'Waiting';
                break;
            case 1: // InProgress
                statusElement.classList.add('bg-warning');
                statusElement.textContent = 'In Progress';
                statusTextElement.textContent = 'Active';
                break;
            case 2: // Completed
                statusElement.classList.add('bg-success');
                statusElement.textContent = 'Completed';
                statusTextElement.textContent = 'Finished';
                break;
        }

        // Update winner
        document.getElementById('winner-name').textContent = 
            tournament.winner ? tournament.winner.name : 'TBD';

        // Update player list
        this.updatePlayerList(tournament.players);

        // Update bracket
        this.updateBracket(tournament);
    }

    updatePlayerList(players) {
        const playerList = document.getElementById('player-list');
        playerList.innerHTML = '';

        players.forEach(player => {
            const li = document.createElement('li');
            li.className = 'list-group-item player-list-item';
            if (player.id === this.currentPlayerId) {
                li.classList.add('active');
            }
            li.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span>${player.name}</span>
                    ${player.id === this.currentPlayerId ? '<small class="text-primary">(You)</small>' : ''}
                </div>
            `;
            playerList.appendChild(li);
        });
    }

    updateBracket(tournament) {
        const bracketContainer = document.getElementById('tournament-bracket');
        
        if (!tournament.matches || tournament.matches.length === 0) {
            this.displayEmptyState();
            return;
        }

        // Group matches by round
        const matchesByRound = {};
        tournament.matches.forEach(match => {
            if (!matchesByRound[match.round]) {
                matchesByRound[match.round] = [];
            }
            matchesByRound[match.round].push(match);
        });

        // Generate bracket HTML
        let bracketHTML = '<div class="bracket">';
        
        Object.keys(matchesByRound).sort((a, b) => parseInt(a) - parseInt(b)).forEach((round, index) => {
            const matches = matchesByRound[round];
            bracketHTML += `
                <div class="bracket-round">
                    <h4>Round ${round}</h4>
                    ${matches.map(match => this.generateMatchHTML(match)).join('')}
                </div>
            `;
            
            // Add connector between rounds (except for last round)
            if (index < Object.keys(matchesByRound).length - 1) {
                bracketHTML += '<div class="bracket-connector"></div>';
            }
        });

        bracketHTML += '</div>';

        // Add winner celebration if tournament is completed
        if (tournament.status === 2 && tournament.winner) {
            bracketHTML += `
                <div class="winner-celebration">
                    <div class="trophy">🏆</div>
                    <h2>Tournament Winner</h2>
                    <h3>${tournament.winner.name}</h3>
                </div>
            `;
        }

        bracketContainer.innerHTML = bracketHTML;
    }

    generateMatchHTML(match) {
        const getStatusClass = () => {
            switch (match.status) {
                case 1: return 'in-progress';
                case 2: return 'completed';
                default: return '';
            }
        };

        const getMoveClass = (move) => {
            switch (move) {
                case 1: return 'move-rock';
                case 2: return 'move-paper';
                case 3: return 'move-scissors';
                default: return 'move-none';
            }
        };

        const getPlayerHTML = (player, move, isWinner = false) => {
            if (!player) {
                return `
                    <div class="player">
                        <span class="player-name">TBD</span>
                        <span class="player-move move-none"></span>
                    </div>
                `;
            }

            return `
                <div class="player ${isWinner ? 'winner' : ''}">
                    <span class="player-name">${player.name}</span>
                    <span class="player-move ${getMoveClass(move)}"></span>
                </div>
            `;
        };

        return `
            <div class="match ${getStatusClass()}" data-match-id="${match.id}">
                ${getPlayerHTML(match.player1, match.player1Move, match.winner?.id === match.player1?.id)}
                <div style="text-align: center; margin: 5px 0; font-size: 0.8em; color: #6c757d;">
                    vs
                </div>
                ${getPlayerHTML(match.player2, match.player2Move, match.winner?.id === match.player2?.id)}
                ${match.status === 2 && match.winner ? 
                    `<div class="text-center mt-2"><small class="text-success">Winner: ${match.winner.name}</small></div>` : 
                    ''}
            </div>
        `;
    }

    displayEmptyState() {
        const bracketContainer = document.getElementById('tournament-bracket');
        bracketContainer.innerHTML = `
            <div class="empty-bracket">
                <h3>No Active Tournament</h3>
                <p>Register players to start a new tournament!</p>
                <div class="loading" style="display: none;"></div>
            </div>
        `;
    }

    showMessage(message, type = 'info') {
        const messageContainer = document.getElementById('register-message');
        messageContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = messageContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    startPeriodicUpdates() {
        // Refresh tournament state every 10 seconds
        setInterval(async () => {
            await this.loadTournamentState();
        }, 10000);
    }

    // Helper method to check if current player has a pending match
    async checkForPendingMatch() {
        if (!this.currentPlayerId) return;

        try {
            const response = await fetch(`/api/players/${this.currentPlayerId}/current-match`);
            if (response.ok) {
                const match = await response.json();
                if (match && match.status !== 2) { // Not completed
                    // Check if player needs to submit a move
                    const playerMove = match.player1?.id === this.currentPlayerId ? 
                        match.player1Move : match.player2Move;
                    
                    if (playerMove === 0) { // Move.None
                        // Show move submission modal
                        const modal = new bootstrap.Modal(document.getElementById('moveModal'));
                        modal.show();
                    }
                }
            }
        } catch (error) {
            console.error('Error checking for pending match:', error);
        }
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentApp = new TournamentApp();
});