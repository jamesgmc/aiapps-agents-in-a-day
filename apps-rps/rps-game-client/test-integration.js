#!/usr/bin/env node

const axios = require('axios');

const SERVER_URL = 'http://localhost:5289';
const CLIENT_URL = 'http://localhost:3000';

async function testBasicConnection() {
    console.log('=== Testing Basic Connection ===\n');
    
    try {
        console.log('Testing server connection...');
        const serverResponse = await axios.get(SERVER_URL);
        console.log('✅ Server is accessible');
        
        console.log('Testing client connection...');
        const clientResponse = await axios.get(CLIENT_URL);
        console.log('✅ Client is accessible');
        
        return true;
    } catch (error) {
        console.error('❌ Connection test failed:', error.message);
        return false;
    }
}

async function testPlayerRegistration() {
    console.log('\n=== Testing Player Registration ===\n');
    
    try {
        const sessionId = 'test-session-' + Date.now();
        
        console.log('Registering test player...');
        const response = await axios.post(`${CLIENT_URL}/register`, {
            playerName: 'Test Player',
            sessionId: sessionId
        });
        
        if (response.data.success) {
            console.log('✅ Player registration successful');
            console.log('Player ID:', response.data.playerId);
            
            // Test status check
            const statusResponse = await axios.get(`${CLIENT_URL}/status?sessionId=${sessionId}`);
            console.log('✅ Status check successful');
            console.log('Player status:', {
                isRegistered: statusResponse.data.isRegistered,
                playerName: statusResponse.data.playerName,
                tournamentStatus: statusResponse.data.tournamentStatus
            });
            
            return {
                playerId: response.data.playerId,
                sessionId: sessionId
            };
        } else {
            console.error('❌ Registration failed:', response.data.error);
            return null;
        }
        
    } catch (error) {
        console.error('❌ Registration test failed:', error.response?.data || error.message);
        return null;
    }
}

async function testServerAPIs() {
    console.log('\n=== Testing Server APIs ===\n');
    
    try {
        console.log('Getting tournament status...');
        const tournamentResponse = await axios.get(`${SERVER_URL}/api/tournament/status`);
        console.log('✅ Tournament API accessible');
        console.log('Tournament status:', {
            status: tournamentResponse.data.status,
            currentRound: tournamentResponse.data.currentRound,
            playersCount: tournamentResponse.data.players.length
        });
        
        // Test player status API (need a valid player ID first)
        const playerData = await testPlayerRegistration();
        if (playerData) {
            console.log('Testing player status API...');
            const playerStatusResponse = await axios.get(`${SERVER_URL}/api/player/${playerData.playerId}/status`);
            console.log('✅ Player status API works');
            console.log('Player tournament status:', {
                tournamentStatus: playerStatusResponse.data.tournamentStatus,
                currentRound: playerStatusResponse.data.currentRound,
                canSubmit: playerStatusResponse.data.canSubmit
            });
        }
        
        return true;
    } catch (error) {
        console.error('❌ Server API test failed:', error.response?.data || error.message);
        return false;
    }
}

async function testManualFlow() {
    console.log('\n=== Manual Testing Flow ===\n');
    
    const playerData = await testPlayerRegistration();
    if (!playerData) {
        console.log('❌ Cannot continue without valid player registration');
        return false;
    }
    
    console.log(`
==================================================
MANUAL TESTING INSTRUCTIONS:
==================================================

1. Open the server UI: ${SERVER_URL}
2. Open the client UI: ${CLIENT_URL}

3. In the server UI:
   - Click "Start Tournament"
   - Click "Start Round" for round 1
   
4. In the client UI:
   - You should see the tournament status update
   - Questions should appear when rounds start
   - You can submit answers manually

5. Test the full flow:
   - Start each of the 5 rounds
   - Submit answers in the client
   - End each round
   - Check results and leaderboard

Your test player:
- Player ID: ${playerData.playerId}
- Session ID: ${playerData.sessionId}

==================================================
    `);
    
    return true;
}

async function main() {
    console.log('RPS Game Client-Server Integration Test\n');
    
    const connectionOK = await testBasicConnection();
    if (!connectionOK) {
        console.log('❌ Basic connection failed. Make sure both server and client are running.');
        process.exit(1);
    }
    
    const serverApisOK = await testServerAPIs();
    if (!serverApisOK) {
        console.log('❌ Server API tests failed.');
        process.exit(1);
    }
    
    await testManualFlow();
    
    console.log('\n✅ Basic integration tests completed successfully!');
    console.log('💡 Follow the manual testing instructions above to test the full tournament flow.');
}

if (require.main === module) {
    main();
}