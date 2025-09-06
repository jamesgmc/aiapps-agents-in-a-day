const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const SERVER_URL = process.env.SERVER_URL || 'http://localhost:5289';

// Middleware
app.use(express.json());
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));

// Game state
let gameState = {
    playerId: null,
    playerName: '',
    isRegistered: false,
    currentRound: 0,
    tournamentStatus: 'Pending',
    roundStatus: null,
    currentQuestion: '',
    gameActive: false,
    results: []
};

// Move enum matching server
const Move = {
    Rock: 0,
    Paper: 1,
    Scissors: 2
};

// API client functions
class GameClient {
    static async registerPlayer(name) {
        try {
            const response = await axios.post(`${SERVER_URL}/api/player/register`, {
                Name: name
            });
            return response.data;
        } catch (error) {
            console.error('Registration error:', error.response?.data || error.message);
            throw error;
        }
    }

    static async getStatus(playerId) {
        try {
            const response = await axios.get(`${SERVER_URL}/api/player/${playerId}/status`);
            return response.data;
        } catch (error) {
            console.error('Status error:', error.response?.data || error.message);
            throw error;
        }
    }

    static async submitAnswer(playerId, roundNumber, answer, move) {
        try {
            const response = await axios.post(`${SERVER_URL}/api/player/submit-answer`, {
                PlayerId: playerId,
                RoundNumber: roundNumber,
                Answer: answer,
                Move: move
            });
            return response.data;
        } catch (error) {
            console.error('Submit error:', error.response?.data || error.message);
            throw error;
        }
    }

    static async getResults(playerId) {
        try {
            const response = await axios.get(`${SERVER_URL}/api/player/${playerId}/results`);
            return response.data;
        } catch (error) {
            console.error('Results error:', error.response?.data || error.message);
            throw error;
        }
    }
}

// Question answering logic (simple pattern matching)
function attemptAnswerQuestion(question) {
    const q = question.toLowerCase();
    
    // Simple answer patterns
    const patterns = {
        '2+2': '4',
        '2 + 2': '4',
        'capital of australia': 'canberra',
        'largest planet': 'jupiter',
        'world war ii end': '1945',
        'chemical symbol for gold': 'au',
        'continents': '7',
        'how many continents': '7',
        'smallest prime': '2',
        'currency of japan': 'yen',
        '10 squared': '100',
        'longest river': 'nile',
        'freezing point': '0',
        'programming language': 'c#',
        'http stand': 'hypertext transfer protocol',
        'speed of light': '299792458',
        'largest ocean': 'pacific',
        'hexagon': '6',
        'square root of 64': '8',
        'capital of france': 'paris',
        'plants absorb': 'carbon dioxide',
        '15% of 200': '30'
    };

    for (const [key, value] of Object.entries(patterns)) {
        if (q.includes(key)) {
            return value;
        }
    }

    // Default fallback answers for common question types
    if (q.includes('what is') && q.includes('+')) return '4';
    if (q.includes('capital')) return 'unknown';
    if (q.includes('year')) return '2000';
    if (q.includes('how many')) return '1';
    
    return 'unknown';
}

// Random move selection
function getRandomMove() {
    const moves = [Move.Rock, Move.Paper, Move.Scissors];
    return moves[Math.floor(Math.random() * moves.length)];
}

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/register', async (req, res) => {
    try {
        const { playerName } = req.body;
        
        if (!playerName) {
            return res.status(400).json({ error: 'Player name is required' });
        }

        const result = await GameClient.registerPlayer(playerName);
        
        gameState.playerId = result.playerId;
        gameState.playerName = playerName;
        gameState.isRegistered = true;
        
        console.log(`Player ${playerName} registered with ID: ${result.PlayerId}`);
        
        res.json({ 
            success: true, 
            playerId: result.playerId, 
            message: result.message 
        });

        // Start monitoring game state
        startGameMonitoring();
        
    } catch (error) {
        res.status(500).json({ 
            error: 'Registration failed', 
            details: error.response?.data?.message || error.message 
        });
    }
});

app.get('/status', (req, res) => {
    res.json(gameState);
});

app.get('/results', async (req, res) => {
    try {
        if (!gameState.playerId) {
            return res.status(400).json({ error: 'Player not registered' });
        }

        const results = await GameClient.getResults(gameState.playerId);
        res.json(results);
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to get results', 
            details: error.message 
        });
    }
});

// Game monitoring and automation
let monitoringInterval = null;
let hasSubmittedForRound = {};

function startGameMonitoring() {
    if (monitoringInterval) {
        clearInterval(monitoringInterval);
    }

    console.log('Starting game monitoring...');
    
    monitoringInterval = setInterval(async () => {
        try {
            if (!gameState.playerId) return;

            const status = await GameClient.getStatus(gameState.playerId);
            
            // Update game state
            gameState.tournamentStatus = status.tournamentStatus;
            gameState.currentRound = status.currentRound;
            gameState.roundStatus = status.currentRoundStatus;
            gameState.currentQuestion = status.currentQuestion;
            gameState.gameActive = status.tournamentStatus === 1; // InProgress

            console.log(`Status: Tournament=${status.tournamentStatus}, Round=${status.currentRound}, RoundStatus=${status.currentRoundStatus}`);

            // If round is in progress and we can submit
            if (status.currentRoundStatus === 1 && status.canSubmit && status.currentQuestion) { // InProgress
                const roundKey = `${status.currentRound}`;
                
                if (!hasSubmittedForRound[roundKey]) {
                    console.log(`Round ${status.currentRound} started with question: ${status.currentQuestion}`);
                    
                    // Attempt to answer the question
                    const answer = attemptAnswerQuestion(status.currentQuestion);
                    const move = getRandomMove();
                    const moveNames = ['Rock', 'Paper', 'Scissors'];
                    
                    console.log(`Submitting answer: "${answer}" and move: ${moveNames[move]}`);
                    
                    try {
                        const result = await GameClient.submitAnswer(
                            gameState.playerId,
                            status.currentRound,
                            answer,
                            move
                        );
                        
                        hasSubmittedForRound[roundKey] = true;
                        console.log(`Submission successful: ${result.message}`);
                        
                    } catch (submitError) {
                        console.error('Failed to submit answer:', submitError.response?.data || submitError.message);
                    }
                }
            }

            // Stop monitoring if tournament is completed
            if (status.tournamentStatus === 2) { // Completed
                console.log('Tournament completed, stopping monitoring');
                clearInterval(monitoringInterval);
                monitoringInterval = null;
            }

        } catch (error) {
            console.error('Monitoring error:', error.message);
        }
    }, 2000); // Check every 2 seconds
}

// Start server
app.listen(PORT, () => {
    console.log(`PSR Game Client running on http://localhost:${PORT}`);
    console.log(`Connecting to game server at: ${SERVER_URL}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down game client...');
    if (monitoringInterval) {
        clearInterval(monitoringInterval);
    }
    process.exit(0);
});