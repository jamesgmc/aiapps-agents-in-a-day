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

        // Auto player registration form
        document.getElementById('auto-register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.registerAutoPlayers();
        });

        // Referee controls
        document.getElementById('start-round-btn').addEventListener('click', async () => {
            await this.startRound();
        });

        document.getElementById('release-results-btn').addEventListener('click', async () => {
            await this.releaseResults();
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

    async registerAutoPlayers() {
        const countInput = document.getElementById('player-count-input');
        const count = parseInt(countInput.value);

        try {
            const response = await fetch('/api/players/register-bulk', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    count: count,
                    useAutoNames: true
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showMessage(result.message, 'success');
                await this.loadTournamentState();
            } else {
                const error = await response.json();
                this.showMessage(error.message || 'Auto registration failed', 'danger');
            }
        } catch (error) {
            console.error('Auto registration error:', error);
            this.showMessage('Network error during auto registration', 'danger');
        }
    }

    async startRound() {
        if (!this.currentTournament) {
            this.showRefereeMessage('No active tournament found', 'danger');
            return;
        }

        try {
            const response = await fetch('/api/tournament/start-round', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    tournamentId: this.currentTournament.tournamentId 
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showRefereeMessage(result.message, 'success');
                await this.loadTournamentState();
            } else {
                const error = await response.json();
                this.showRefereeMessage(error.message || 'Failed to start round', 'danger');
            }
        } catch (error) {
            console.error('Start round error:', error);
            this.showRefereeMessage('Network error during round start', 'danger');
        }
    }

    async releaseResults() {
        if (!this.currentTournament) {
            this.showRefereeMessage('No active tournament found', 'danger');
            return;
        }

        try {
            const response = await fetch('/api/tournament/release-results', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    tournamentId: this.currentTournament.tournamentId 
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showRefereeMessage(result.message, 'success');
                await this.loadTournamentState();
            } else {
                const error = await response.json();
                this.showRefereeMessage(error.message || 'Failed to release results', 'danger');
            }
        } catch (error) {
            console.error('Release results error:', error);
            this.showRefereeMessage('Network error during result release', 'danger');
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
        document.getElementById('round-info').textContent = tournament.currentRound;
        
        // Update round status
        const roundStatusElement = document.getElementById('round-status');
        switch (tournament.currentRoundStatus) {
            case 0: // Waiting
                roundStatusElement.textContent = 'Waiting';
                roundStatusElement.className = 'text-secondary';
                break;
            case 1: // InProgress
                roundStatusElement.textContent = 'In Progress';
                roundStatusElement.className = 'text-warning';
                break;
            case 2: // ResultsAvailable
                roundStatusElement.textContent = 'Results Available';
                roundStatusElement.className = 'text-info';
                break;
            case 3: // Completed
                roundStatusElement.textContent = 'Completed';
                roundStatusElement.className = 'text-success';
                break;
        }
        
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
        
        // Update referee controls
        this.updateRefereeControls(tournament);
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

        // Check if moves should be visible based on round status
        const shouldShowMoves = () => {
            if (!this.currentTournament) return false;
            
            // Show moves only if:
            // 1. Match is completed AND
            // 2. Results have been released (ResultsAvailable or Completed) OR tournament is finished
            return match.status === 2 && 
                   (this.currentTournament.currentRoundStatus >= 2 || this.currentTournament.status === 2);
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

            const moveDisplay = shouldShowMoves() ? getMoveClass(move) : 
                                (move !== 0 ? 'move-submitted' : 'move-none');

            return `
                <div class="player ${isWinner ? 'winner' : ''}">
                    <span class="player-name">${player.name}</span>
                    <span class="player-move ${moveDisplay}"></span>
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
                ${match.status === 2 && match.winner && shouldShowMoves() ? 
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

    showRefereeMessage(message, type = 'info') {
        const messageContainer = document.getElementById('referee-message');
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

    updateRefereeControls(tournament) {
        const startRoundBtn = document.getElementById('start-round-btn');
        const releaseResultsBtn = document.getElementById('release-results-btn');
        
        // Reset button states
        startRoundBtn.disabled = true;
        releaseResultsBtn.disabled = true;
        
        if (tournament.status !== 1) { // Not in progress
            return;
        }
        
        // Check current round status to determine which buttons to enable
        switch (tournament.currentRoundStatus) {
            case 0: // Waiting - can start round
                startRoundBtn.disabled = false;
                break;
            case 1: // InProgress - check if all matches are completed
                const currentRoundMatches = tournament.matches.filter(m => m.round === tournament.currentRound);
                if (currentRoundMatches.length > 0 && currentRoundMatches.every(m => m.status === 2)) {
                    releaseResultsBtn.disabled = false;
                }
                break;
            case 2: // ResultsAvailable - results have been released
                // Could advance to next round automatically or wait for referee action
                break;
        }
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