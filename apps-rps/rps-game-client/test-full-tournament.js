#!/usr/bin/env node

const axios = require('axios');
const { spawn } = require('child_process');
const path = require('path');

const SERVER_URL = 'http://localhost:5289';
const CLIENT_URL = 'http://localhost:3000';

class TournamentTester {
    constructor() {
        this.serverProcess = null;
        this.clientProcess = null;
        this.playerId = null;
        this.sessionId = null;
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async waitForServer(url, maxAttempts = 30) {
        console.log(`Waiting for server at ${url}...`);
        for (let i = 0; i < maxAttempts; i++) {
            try {
                await axios.get(url);
                console.log(`Server at ${url} is ready!`);
                return true;
            } catch (error) {
                if (i === maxAttempts - 1) {
                    throw new Error(`Server at ${url} failed to start after ${maxAttempts} attempts`);
                }
                await this.sleep(2000);
            }
        }
    }

    async startServer() {
        console.log('Starting RPS Game Server...');
        this.serverProcess = spawn('dotnet', ['run'], {
            cwd: '../rps-game-server',
            stdio: 'pipe'
        });

        this.serverProcess.stdout.on('data', (data) => {
            console.log(`[SERVER] ${data.toString().trim()}`);
        });

        this.serverProcess.stderr.on('data', (data) => {
            console.log(`[SERVER ERROR] ${data.toString().trim()}`);
        });

        await this.waitForServer(SERVER_URL);
    }

    async startClient() {
        console.log('Starting RPS Game Client...');
        this.clientProcess = spawn('node', ['server.js'], {
            stdio: 'pipe'
        });

        this.clientProcess.stdout.on('data', (data) => {
            console.log(`[CLIENT] ${data.toString().trim()}`);
        });

        this.clientProcess.stderr.on('data', (data) => {
            console.log(`[CLIENT ERROR] ${data.toString().trim()}`);
        });

        await this.waitForServer(CLIENT_URL);
    }

    async registerPlayer() {
        console.log('Registering test player...');
        const response = await axios.post(`${CLIENT_URL}/register`, {
            playerName: 'Test Player',
            sessionId: 'test-session-123'
        });

        if (response.data.success) {
            this.playerId = response.data.playerId;
            this.sessionId = 'test-session-123';
            console.log(`Player registered with ID: ${this.playerId}`);
            return true;
        } else {
            throw new Error('Failed to register player: ' + response.data.error);
        }
    }

    async getPlayerStatus() {
        const response = await axios.get(`${CLIENT_URL}/status?sessionId=${this.sessionId}`);
        return response.data;
    }

    async startTournament() {
        console.log('Starting tournament...');
        try {
            const response = await axios.post(`${SERVER_URL}/StartTournament`, {}, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            console.log('Tournament started successfully');
            return true;
        } catch (error) {
            console.log('Tournament start failed:', error.response?.data || error.message);
            return false;
        }
    }

    async startRound(roundNumber) {
        console.log(`Starting round ${roundNumber}...`);
        try {
            // Use form-encoded data for MVC endpoint
            const params = new URLSearchParams();
            params.append('roundNumber', roundNumber);
            
            const response = await axios.post(`${SERVER_URL}/StartRound`, params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            console.log(`Round ${roundNumber} started successfully`);
            return true;
        } catch (error) {
            console.log(`Round start failed for round ${roundNumber}, error:`, error.response?.data || error.message);
            return false;
        }
    }

    async endRound(roundNumber) {
        console.log(`Ending round ${roundNumber}...`);
        try {
            const params = new URLSearchParams();
            params.append('roundNumber', roundNumber);
            
            const response = await axios.post(`${SERVER_URL}/EndRound`, params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });
            console.log(`Round ${roundNumber} ended successfully`);
            return true;
        } catch (error) {
            console.log(`Round end failed for round ${roundNumber}, error:`, error.response?.data || error.message);
            return false;
        }
    }

    async submitAnswer(roundNumber, answer, move) {
        console.log(`Submitting answer for round ${roundNumber}: "${answer}", move: ${move}`);
        try {
            const response = await axios.post(`${CLIENT_URL}/submit-answer`, {
                playerId: this.playerId,
                roundNumber: roundNumber,
                answer: answer,
                move: move,
                sessionId: this.sessionId
            });
            
            if (response.data.success) {
                console.log(`Answer submitted successfully for round ${roundNumber}`);
                return true;
            } else {
                console.log(`Answer submission failed:`, response.data.error);
                return false;
            }
        } catch (error) {
            console.log(`Answer submission error:`, error.response?.data || error.message);
            return false;
        }
    }

    async runFullTournament() {
        try {
            console.log('=== Starting Full Tournament Test ===\n');

            // Start services
            await this.startServer();
            await this.sleep(3000); // Give server time to fully initialize
            
            await this.startClient();
            await this.sleep(2000); // Give client time to start

            // Register player
            await this.registerPlayer();
            await this.sleep(1000);

            // Check initial status
            let status = await this.getPlayerStatus();
            console.log('Initial player status:', status);

            // Start tournament
            await this.startTournament();
            await this.sleep(2000);

            // Run 5 rounds
            for (let round = 1; round <= 5; round++) {
                console.log(`\n=== Round ${round} ===`);
                
                // Start the round
                await this.startRound(round);
                await this.sleep(2000);

                // Check status and get question
                status = await this.getPlayerStatus();
                console.log(`Round ${round} status:`, {
                    tournamentStatus: status.tournamentStatus,
                    currentRound: status.currentRound,
                    roundStatus: status.roundStatus,
                    question: status.currentQuestion
                });

                // Submit answer if round is active
                if (status.currentQuestion) {
                    const answer = this.generateAnswer(status.currentQuestion);
                    const move = Math.floor(Math.random() * 3); // 0=Rock, 1=Paper, 2=Scissors
                    
                    await this.submitAnswer(round, answer, move);
                    await this.sleep(1000);
                }

                // End the round
                await this.endRound(round);
                await this.sleep(2000);
            }

            // Check final results
            console.log('\n=== Final Results ===');
            const finalResults = await axios.get(`${CLIENT_URL}/final-results?sessionId=${this.sessionId}`);
            console.log('Final tournament results:', finalResults.data);

            console.log('\n=== Tournament Test Completed Successfully! ===');
            return true;

        } catch (error) {
            console.error('Tournament test failed:', error.message);
            if (error.response?.data) {
                console.error('Response data:', error.response.data);
            }
            return false;
        }
    }

    generateAnswer(question) {
        // Simple answer generation based on question patterns
        const q = question.toLowerCase();
        
        if (q.includes('2+2') || q.includes('2 + 2')) return '4';
        if (q.includes('capital of australia')) return 'canberra';
        if (q.includes('largest planet')) return 'jupiter';
        if (q.includes('world war') && q.includes('end')) return '1945';
        if (q.includes('chemical symbol') && q.includes('gold')) return 'au';
        if (q.includes('continents')) return '7';
        if (q.includes('smallest prime')) return '2';
        if (q.includes('currency') && q.includes('japan')) return 'yen';
        if (q.includes('squared') || q.includes('10²')) return '100';
        if (q.includes('longest river')) return 'nile';
        if (q.includes('freezing point')) return '0';
        if (q.includes('speed of light')) return '299792458';
        if (q.includes('largest ocean')) return 'pacific';
        if (q.includes('hexagon')) return '6';
        if (q.includes('square root') && q.includes('64')) return '8';
        if (q.includes('capital') && q.includes('france')) return 'paris';
        
        return 'unknown'; // fallback
    }

    async cleanup() {
        console.log('Cleaning up processes...');
        
        if (this.clientProcess) {
            this.clientProcess.kill();
        }
        
        if (this.serverProcess) {
            this.serverProcess.kill();
        }

        // Wait a bit for processes to clean up
        await this.sleep(2000);
    }
}

// Run the test
async function main() {
    const tester = new TournamentTester();
    
    try {
        const success = await tester.runFullTournament();
        if (success) {
            console.log('✅ All tests passed!');
            process.exit(0);
        } else {
            console.log('❌ Tests failed!');
            process.exit(1);
        }
    } catch (error) {
        console.error('Test execution failed:', error);
        process.exit(1);
    } finally {
        await tester.cleanup();
    }
}

// Handle process termination gracefully
process.on('SIGINT', async () => {
    console.log('\nReceived SIGINT, cleaning up...');
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('\nReceived SIGTERM, cleaning up...');
    process.exit(0);
});

if (require.main === module) {
    main();
}

module.exports = TournamentTester;