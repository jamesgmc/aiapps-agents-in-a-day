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
        document.getElementById('start-match-btn').addEventListener('click', async () => {
            await this.startRound();
        });

        document.getElementById('start-round-btn').addEventListener('click', async () => {
            await this.startMatchRound();
        });

        document.getElementById('release-round-results-btn').addEventListener('click', async () => {
            await this.releaseMatchRoundResults();
        });

        document.getElementById('release-match-results-btn').addEventListener('click', async () => {
            await this.releaseMatchResults();
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

    async releaseMatchResults() {
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
                this.showRefereeMessage(error.message || 'Failed to release match results', 'danger');
            }
        } catch (error) {
            console.error('Release match results error:', error);
            this.showRefereeMessage('Network error during match result release', 'danger');
        }
    }

    async startMatchRound() {
        const selectedMatch = this.getSelectedMatch();
        if (!selectedMatch) {
            this.showRefereeMessage('Please select a match to start a round', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/tournament/start-match-round', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    matchId: selectedMatch.id 
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showRefereeMessage(result.message, 'success');
                await this.loadTournamentState();
            } else {
                const error = await response.json();
                this.showRefereeMessage(error.message || 'Failed to start match round', 'danger');
            }
        } catch (error) {
            console.error('Start match round error:', error);
            this.showRefereeMessage('Network error during match round start', 'danger');
        }
    }

    async releaseMatchRoundResults() {
        const selectedMatch = this.getSelectedMatch();
        if (!selectedMatch) {
            this.showRefereeMessage('Please select a match to release round results', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/tournament/release-match-round-results', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    matchId: selectedMatch.id 
                })
            });

            if (response.ok) {
                const result = await response.json();
                this.showRefereeMessage(result.message, 'success');
                await this.loadTournamentState();
            } else {
                const error = await response.json();
                this.showRefereeMessage(error.message || 'Failed to release round results', 'danger');
            }
        } catch (error) {
            console.error('Release match round results error:', error);
            this.showRefereeMessage('Network error during round result release', 'danger');
        }
    }

    getSelectedMatch() {
        // For now, return the first active match found
        // In a more sophisticated UI, this would be based on user selection
        if (!this.currentTournament || !this.currentTournament.matches) {
            return null;
        }

        return this.currentTournament.matches.find(match => 
            match.status !== 2 && // Not completed
            match.currentRoundStatus !== undefined
        );
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

        const getMoveSymbol = (move) => {
            switch (move) {
                case 1: return '🪨';
                case 2: return '📄';
                case 3: return '✂️';
                default: return '';
            }
        };

        const getPlayerHTML = (player, isWinner = false) => {
            if (!player) {
                return `
                    <div class="player">
                        <span class="player-name">TBD</span>
                    </div>
                `;
            }

            return `
                <div class="player ${isWinner ? 'winner' : ''}">
                    <span class="player-name">${player.name}</span>
                </div>
            `;
        };

        // Generate rounds display
        let roundsHTML = '';
        if (match.matchRounds && match.matchRounds.length > 0) {
            roundsHTML = `
                <div class="match-rounds">
                    <div class="rounds-header">Rounds (Best of 3)</div>
                    <div class="rounds-grid">
                        ${match.matchRounds.map(round => `
                            <div class="round ${round.status === 2 ? 'completed' : ''}">
                                <div class="round-header">Round ${round.roundNumber}</div>
                                <div class="round-moves">
                                    <div class="move">${round.status === 2 ? getMoveSymbol(round.player1Move) : (round.player1Move !== 0 ? '✓' : '')}</div>
                                    <div class="vs">vs</div>
                                    <div class="move">${round.status === 2 ? getMoveSymbol(round.player2Move) : (round.player2Move !== 0 ? '✓' : '')}</div>
                                </div>
                                ${round.status === 2 && round.winner ? 
                                    `<div class="round-winner">Winner: ${round.winner.name}</div>` : 
                                    ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        // Current round status
        let currentRoundStatus = '';
        if (match.status !== 2) {
            currentRoundStatus = `
                <div class="current-round-status">
                    Current Round: ${match.currentRoundNumber}/3
                    <span class="status-badge ${match.currentRoundStatus === 0 ? 'waiting' : match.currentRoundStatus === 1 ? 'in-progress' : 'completed'}">
                        ${match.currentRoundStatus === 0 ? 'Waiting' : match.currentRoundStatus === 1 ? 'In Progress' : 'Completed'}
                    </span>
                </div>
            `;
        }

        return `
            <div class="match ${getStatusClass()}" data-match-id="${match.id}">
                <div class="match-header">
                    ${getPlayerHTML(match.player1, match.winner?.id === match.player1?.id)}
                    <div style="text-align: center; margin: 5px 0; font-size: 0.8em; color: #6c757d;">
                        vs
                    </div>
                    ${getPlayerHTML(match.player2, match.winner?.id === match.player2?.id)}
                </div>
                ${currentRoundStatus}
                ${roundsHTML}
                ${match.status === 2 && match.winner ? 
                    `<div class="text-center mt-2"><strong class="text-success">Match Winner: ${match.winner.name}</strong></div>` : 
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
        const startRoundBtn = document.getElementById('start-match-btn');
        const startMatchRoundBtn = document.getElementById('start-round-btn');
        const releaseMatchRoundResultsBtn = document.getElementById('release-round-results-btn');
        const releaseResultsBtn = document.getElementById('release-match-results-btn');
        
        // Reset button states
        startRoundBtn.disabled = true;
        startMatchRoundBtn.disabled = true;
        releaseMatchRoundResultsBtn.disabled = true;
        releaseResultsBtn.disabled = true;
        
        if (tournament.status !== 1) { // Not in progress
            return;
        }
        
        // Check current tournament round status
        switch (tournament.currentRoundStatus) {
            case 0: // Waiting - can start tournament round
                startRoundBtn.disabled = false;
                break;
            case 1: // InProgress - check if all matches are completed
                const currentRoundMatches = tournament.matches.filter(m => m.round === tournament.currentRound);
                if (currentRoundMatches.length > 0 && currentRoundMatches.every(m => m.status === 2)) {
                    releaseResultsBtn.disabled = false;
                }
                
                // Check for matches with rounds that can be started or have results to release
                currentRoundMatches.forEach(match => {
                    if (match.status !== 2) { // Match not completed
                        if (match.currentRoundStatus === 0) { // Round waiting
                            startMatchRoundBtn.disabled = false;
                        } else if (match.currentRoundStatus === 1) { // Round in progress
                            // Check if current round is ready for results
                            const currentRound = match.matchRounds?.find(r => r.roundNumber === match.currentRoundNumber);
                            if (currentRound && this.isRoundReadyForResults(currentRound)) {
                                releaseMatchRoundResultsBtn.disabled = false;
                            }
                        }
                    }
                });
                break;
            case 2: // ResultsAvailable - results have been released
                // Could advance to next round automatically or wait for referee action
                break;
        }
    }

    isRoundReadyForResults(round) {
        // Check if both players have submitted moves for this round
        return round.player1Move !== 0 && round.player2Move !== 0; // Move.None = 0
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

// Navigation functions
function showTournament() {
    document.getElementById('tournament-page').style.display = 'block';
    document.getElementById('matches-page').style.display = 'none';
    
    // Update navigation active state
    document.getElementById('nav-tournament').classList.add('active');
    document.getElementById('nav-matches').classList.remove('active');
}

function showMatches() {
    document.getElementById('tournament-page').style.display = 'none';
    document.getElementById('matches-page').style.display = 'block';
    
    // Update navigation active state
    document.getElementById('nav-tournament').classList.remove('active');
    document.getElementById('nav-matches').classList.add('active');
    
    // Load matches data
    loadMatchesData();
}

// Load matches data from API
async function loadMatchesData() {
    const loadingElement = document.getElementById('matches-loading');
    const errorElement = document.getElementById('matches-error');
    const tableBody = document.getElementById('matches-table-body');
    
    try {
        // Show loading spinner
        loadingElement.style.display = 'block';
        errorElement.style.display = 'none';
        tableBody.innerHTML = '';
        
        const response = await fetch('/api/tournament/matches');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const matches = await response.json();
        
        // Hide loading spinner
        loadingElement.style.display = 'none';
        
        // Populate table
        tableBody.innerHTML = matches.map(match => {
            const formatMove = (move) => {
                switch (move) {
                    case 1: return '🪨 Rock';
                    case 2: return '📄 Paper';
                    case 3: return '✂️ Scissors';
                    default: return '-';
                }
            };
            
            const formatStatus = (status) => {
                switch (status) {
                    case 0: return '<span class="badge bg-secondary">Pending</span>';
                    case 1: return '<span class="badge bg-warning">In Progress</span>';
                    case 2: return '<span class="badge bg-success">Completed</span>';
                    default: return '<span class="badge bg-light">Unknown</span>';
                }
            };
            
            const formatDate = (dateString) => {
                if (!dateString) return '-';
                return new Date(dateString).toLocaleString();
            };
            
            return `
                <tr>
                    <td>${match.id}</td>
                    <td>${match.tournamentId}</td>
                    <td>${match.round}</td>
                    <td>${match.player1?.name || 'TBD'}</td>
                    <td>${formatMove(match.player1Move)}</td>
                    <td>${match.player2?.name || 'TBD'}</td>
                    <td>${formatMove(match.player2Move)}</td>
                    <td>${match.winner?.name || '-'}</td>
                    <td>${formatStatus(match.status)}</td>
                    <td>${formatDate(match.createdAt)}</td>
                    <td>${formatDate(match.completedAt)}</td>
                </tr>
            `;
        }).join('');
        
        if (matches.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="11" class="text-center">No matches found</td></tr>';
        }
        
    } catch (error) {
        console.error('Error loading matches:', error);
        loadingElement.style.display = 'none';
        errorElement.style.display = 'block';
        errorElement.textContent = 'Error loading match data: ' + error.message;
    }
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.tournamentApp = new TournamentApp();
});