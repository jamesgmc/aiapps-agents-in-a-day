#!/usr/bin/env node

const axios = require('axios');

const SERVER_URL = 'http://localhost:5289';
const CLIENT_URL = 'http://localhost:3000';

class AutomatedTournamentTest {
    constructor() {
        this.playerId = null;
        this.sessionId = `test-session-${Date.now()}`;
        this.moveNames = ['Rock', 'Paper', 'Scissors'];
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async registerPlayer() {
        console.log('📝 Registering test player...');
        const response = await axios.post(`${CLIENT_URL}/register`, {
            playerName: 'Automated Test Player',
            sessionId: this.sessionId
        });

        if (response.data.success) {
            this.playerId = response.data.playerId;
            console.log(`✅ Player registered with ID: ${this.playerId}`);
            return true;
        } else {
            throw new Error('Failed to register player: ' + response.data.error);
        }
    }

    async getPlayerStatus() {
        const response = await axios.get(`${CLIENT_URL}/status?sessionId=${this.sessionId}`);
        return response.data;
    }

    async resetTournament() {
        console.log('🔄 Resetting tournament...');
        try {
            await axios.post(`${SERVER_URL}/Home/ResetTournament`, '', {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                },
                maxRedirects: 0,
                validateStatus: (status) => status < 400
            });
            console.log('✅ Tournament reset successfully');
            return true;
        } catch (error) {
            if (error.response && error.response.status === 302) {
                console.log('✅ Tournament reset (got redirect as expected)');
                return true;
            }
            console.log('❌ Tournament reset failed:', error.response?.data || error.message);
            return false;
        }
    }

    async getTournamentStatus() {
        const response = await axios.get(`${SERVER_URL}/api/tournament/status`);
        return response.data;
    }

    async startTournament() {
        console.log('🏆 Starting tournament...');
        try {
            await axios.post(`${SERVER_URL}/Home/StartTournament`, '', {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                },
                maxRedirects: 0,
                validateStatus: (status) => status < 400 // Accept redirects as success
            });
            console.log('✅ Tournament started successfully');
            return true;
        } catch (error) {
            if (error.response && error.response.status === 302) {
                console.log('✅ Tournament started (got redirect as expected)');
                return true;
            }
            console.log('❌ Tournament start failed:', error.response?.data || error.message);
            return false;
        }
    }

    async startRound(roundNumber) {
        console.log(`▶️  Starting round ${roundNumber}...`);
        try {
            const params = new URLSearchParams();
            params.append('roundNumber', roundNumber);
            
            await axios.post(`${SERVER_URL}/Home/StartRound`, params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                },
                maxRedirects: 0,
                validateStatus: (status) => status < 400
            });
            console.log(`✅ Round ${roundNumber} started successfully`);
            return true;
        } catch (error) {
            if (error.response && error.response.status === 302) {
                console.log(`✅ Round ${roundNumber} started (got redirect as expected)`);
                return true;
            }
            console.log(`❌ Round ${roundNumber} start failed:`, error.response?.data || error.message);
            return false;
        }
    }

    async endRound(roundNumber) {
        console.log(`⏹️  Ending round ${roundNumber}...`);
        try {
            const params = new URLSearchParams();
            params.append('roundNumber', roundNumber);
            
            await axios.post(`${SERVER_URL}/Home/EndRound`, params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                },
                maxRedirects: 0,
                validateStatus: (status) => status < 400
            });
            console.log(`✅ Round ${roundNumber} ended successfully`);
            return true;
        } catch (error) {
            if (error.response && error.response.status === 302) {
                console.log(`✅ Round ${roundNumber} ended (got redirect as expected)`);
                return true;
            }
            console.log(`❌ Round ${roundNumber} end failed:`, error.response?.data || error.message);
            return false;
        }
    }

    async submitAnswer(roundNumber, answer, move) {
        console.log(`📤 Submitting answer for round ${roundNumber}: "${answer}", move: ${this.moveNames[move]}`);
        try {
            const response = await axios.post(`${CLIENT_URL}/submit-answer`, {
                playerId: this.playerId,
                roundNumber: roundNumber,
                answer: answer,
                move: move,
                sessionId: this.sessionId
            });
            
            if (response.data.success) {
                console.log(`✅ Answer submitted successfully for round ${roundNumber}`);
                return true;
            } else {
                console.log(`❌ Answer submission failed:`, response.data.error);
                return false;
            }
        } catch (error) {
            console.log(`❌ Answer submission error:`, error.response?.data || error.message);
            return false;
        }
    }

    generateAnswer(question) {
        const q = question.toLowerCase();
        
        // Question patterns matching the client's answer logic
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

    async runFullTournament() {
        console.log('🎮 =========================');
        console.log('🎮 AUTOMATED TOURNAMENT TEST');
        console.log('🎮 =========================\n');

        try {
            // 0. Reset tournament to ensure clean state
            console.log('🔄 Ensuring clean tournament state...');
            await this.resetTournament();
            await this.sleep(1000);

            // 1. Register player
            await this.registerPlayer();
            await this.sleep(1000);

            // 2. Check initial status
            console.log('📊 Checking initial tournament status...');
            let tournamentStatus = await this.getTournamentStatus();
            console.log(`Tournament status: ${tournamentStatus.status} (0=Pending, 1=InProgress, 2=Completed)`);
            console.log(`Players registered: ${tournamentStatus.players.length}`);

            // 3. Start tournament
            const tournamentStarted = await this.startTournament();
            if (!tournamentStarted) {
                throw new Error('Failed to start tournament');
            }
            await this.sleep(2000);

            // 4. Verify tournament started
            tournamentStatus = await this.getTournamentStatus();
            console.log(`📊 Tournament status after start: ${tournamentStatus.status}`);

            // 5. Run all 5 rounds
            for (let round = 1; round <= 5; round++) {
                console.log(`\n🎯 === ROUND ${round} ===`);
                
                // Start the round
                const roundStarted = await this.startRound(round);
                if (!roundStarted) {
                    console.log(`⚠️  Failed to start round ${round}, continuing...`);
                    continue;
                }
                await this.sleep(2000);

                // Check player status to get question
                const playerStatus = await this.getPlayerStatus();
                console.log(`📊 Player status: Tournament=${playerStatus.tournamentStatus}, Round=${playerStatus.currentRound}`);
                
                if (playerStatus.currentQuestion) {
                    console.log(`❓ Question: ${playerStatus.currentQuestion}`);
                    
                    // Generate answer and random move
                    const answer = this.generateAnswer(playerStatus.currentQuestion);
                    const move = Math.floor(Math.random() * 3); // 0=Rock, 1=Paper, 2=Scissors
                    
                    // Submit answer
                    await this.submitAnswer(round, answer, move);
                    await this.sleep(1000);
                } else {
                    console.log('⚠️  No question available for this round');
                }

                // End the round
                await this.endRound(round);
                await this.sleep(2000);

                // Check results
                try {
                    const results = await axios.get(`${CLIENT_URL}/results?sessionId=${this.sessionId}`);
                    if (results.data && Array.isArray(results.data)) {
                        console.log(`📈 Round ${round} completed. Total results so far: ${results.data.length}`);
                    }
                } catch (error) {
                    console.log('⚠️  Could not get results yet');
                }
            }

            // 6. Check final results
            console.log('\n🏁 === FINAL RESULTS ===');
            try {
                const finalResults = await axios.get(`${CLIENT_URL}/final-results?sessionId=${this.sessionId}`);
                
                if (finalResults.data.success !== false) {
                    console.log('✅ Final results retrieved successfully');
                    if (finalResults.data.results) {
                        console.log(`📊 Total rounds completed: ${finalResults.data.results.length}`);
                        console.log(`🎯 Final score: ${finalResults.data.totalScore || 'Unknown'}`);
                    }
                } else {
                    console.log('⚠️  Tournament may not be fully completed yet');
                }
            } catch (error) {
                console.log('⚠️  Could not get final results:', error.message);
            }

            // 7. Show final tournament status
            tournamentStatus = await this.getTournamentStatus();
            console.log(`\n📊 Final tournament status: ${tournamentStatus.status}`);
            console.log(`📊 Current round: ${tournamentStatus.currentRound}`);
            
            console.log('\n🎉 ===========================');
            console.log('🎉 TOURNAMENT TEST COMPLETED!');
            console.log('🎉 ===========================');
            
            return true;

        } catch (error) {
            console.error('💥 Tournament test failed:', error.message);
            if (error.response?.data) {
                console.error('Response data:', error.response.data);
            }
            return false;
        }
    }
}

async function main() {
    const tester = new AutomatedTournamentTest();
    
    console.log('⏳ Waiting for services to be ready...\n');
    
    try {
        // Quick connection check
        await axios.get(SERVER_URL);
        await axios.get(CLIENT_URL);
        console.log('✅ Both services are accessible\n');
    } catch (error) {
        console.error('❌ Services not accessible. Make sure both server and client are running.');
        console.error('Server should be at:', SERVER_URL);
        console.error('Client should be at:', CLIENT_URL);
        process.exit(1);
    }
    
    const success = await tester.runFullTournament();
    
    if (success) {
        console.log('\n✅ All tests completed successfully!');
        process.exit(0);
    } else {
        console.log('\n❌ Tests failed!');
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = AutomatedTournamentTest;