# 🪨📄✂️ Rock-Paper-Scissors Tournament Game Rule Book

Welcome to the ultimate digital arena where strategy meets chance, and legends are born with the simple throw of a hand! This comprehensive guide will walk you through every aspect of our thrilling Rock-Paper-Scissors tournament system.

## 🎯 Game Overview

Our tournament system brings the classic game of Rock-Paper-Scissors into the digital age with an exciting **8-player elimination tournament** format. Players from around the world can join via our API, compete in real-time rounds, and climb their way to becoming the ultimate champion!

### 🏆 Tournament Objective
- **Goal**: Be the last player standing after three elimination rounds
- **Format**: Single-elimination bracket with 8 players
- **Structure**: Round 1 (8→4) → Round 2 (4→2) → Round 3 (2→1)
- **Victory**: Strategic thinking, quick reflexes, and a touch of luck!

## 👥 Roles and Responsibilities

### 🎮 The Player
**The Competitor** - You are the heart of the tournament!

**Responsibilities:**
- Register for tournaments using your chosen name
- Submit moves (Rock, Paper, or Scissors) when prompted
- Stay active and responsive during your matches
- Celebrate victories and learn from defeats!

**Powers:**
- Choose your battle strategy
- Represent your gaming prowess
- Build your tournament reputation

### 🖥️ The Client
**The Gateway** - Your digital representative in the tournament realm!

**Responsibilities:**
- Connect to the tournament server via API
- Register players with unique identities
- Submit player moves to the server
- Poll for round status and match updates
- Handle player simulation for automated gameplay

**Capabilities:**
- Auto-generate creative player names
- Support multiple player simulations
- Provide real-time tournament monitoring
- Handle network resilience and error recovery

### 🎪 The Server
**The Tournament Master** - The central command that orchestrates the entire competition!

**Responsibilities:**
- Manage player registrations and unique ID assignments
- Create and oversee tournament brackets
- Process move submissions and determine round winners
- Maintain game state and round progression
- Provide real-time updates to all participants
- Serve the referee interface for tournament control

**Powers:**
- Generate tournament brackets automatically
- Calculate match outcomes using official RPS rules
- Broadcast live updates via SignalR
- Maintain complete tournament history and statistics

### 🦓 The Referee
**The Tournament Director** - The human overseer ensuring fair play!

**Responsibilities:**
- Monitor tournament progress via the web interface
- Control round timing and progression
- Start new rounds when all players are ready
- Release match results at the appropriate time
- Ensure tournament integrity and fair play

**Controls:**
- **Start Round Button**: Initiates a new tournament round
- **Show Results Button**: Reveals round outcomes to all participants
- **Tournament Dashboard**: Real-time monitoring of all matches and players

## 🚀 Getting Started: Player Registration

### 🎪 The Registration Arena

Before you can throw your first Rock, you need to enter the tournament! Here's how the magic happens:

#### 📝 Registration Process

1. **Client Connection**: Your client connects to the tournament server
2. **Player Creation**: Choose your warrior name or let the system generate one
3. **Unique ID Assignment**: Server assigns you a unique player number (your tournament identity)
4. **Tournament Placement**: You're automatically assigned to the next available tournament
5. **Ready Status**: Wait for 7 other brave souls to join your tournament


## 🏟️ Tournament Structure

### 🎯 The 8-Player Elimination Bracket

Our tournament follows a classic elimination format designed for maximum excitement.
There are 3 matches in each round, and the winner of most wins advances to the next round.

```
Round 1: The Opening Battles
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│Player 1 │    │Player 3 │    │Player 5 │    │Player 7 │
│    vs   │    │    vs   │    │    vs   │    │    vs   │
│Player 2 │    │Player 4 │    │Player 6 │    │Player 8 │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
     │              │              │              │
     ▼              ▼              ▼              ▼
  Winner A       Winner B       Winner C       Winner D

Round 2: The Semi-Finals
┌─────────┐                    ┌─────────┐
│Winner A │                    │Winner C │
│    vs   │                    │    vs   │
│Winner B │                    │Winner D │
└─────────┘                    └─────────┘
     │                              │
     ▼                              ▼
  Finalist 1                   Finalist 2

Round 3: The Championship
┌─────────┐
│Finalist1│
│    vs   │
│Finalist2│
└─────────┘
     │
     ▼
  🏆 CHAMPION! 🏆
```



## 🎮 Game Process

### 🚀 Starting the Tournament

- Run the server side in `#file:apps/psr-game-server` using dotnet, and ensure the frontend webpage is accessible
- Run `#file:apps/psr-game-client/main.py` multiple times to simulate 8 players in the tournament
- All clients should be able to register themselves to the tournament
- Once all 8 players are registered, the psr-game-server's web page should be ready to start the tournament
- The **[Start Round 1]** button should be enabled

### 🥊 Round 1: The Opening Battles (8 Players → 4 Winners)

Round 1 consists of **4 simultaneous matches** where each pair of players competes in a **best-of-3 series**:

#### 🎯 Match Structure in Round 1

- **Match 1**: Player 1 vs Player 2
- **Match 2**: Player 3 vs Player 4  
- **Match 3**: Player 5 vs Player 6
- **Match 4**: Player 7 vs Player 8

#### 🎲 Best-of-3 Series Process

Each match consists of 3 individual Rock-Paper-Scissors games:

**Starting Match 1:**

1. Click **[Start Round 1]** button to begin the round
2. Click **[Start Match]** button to start Game 1 of Match 1
3. Once **[Start Match]** is clicked, Player 1 and Player 2 can submit their moves for Game 1
4. When both players have submitted moves, **[Release Match Results]** button becomes enabled
5. Click **[Release Match Results]** to display the winner of Game 1

**Continuing the Best-of-3:**

6. Repeat steps 2-5 for Game 2 of Match 1
7. Repeat steps 2-5 for Game 3 of Match 1 (if needed)
8. The player who wins 2 out of 3 games wins Match 1

**Completing All Matches:**

9. Repeat the entire best-of-3 process for Match 2 (Player 3 vs Player 4)
10. Repeat the entire best-of-3 process for Match 3 (Player 5 vs Player 6)
11. Repeat the entire best-of-3 process for Match 4 (Player 7 vs Player 8)
12. Once all 4 matches are completed, **[Release Round Results]** button becomes enabled
13. Click **[Release Round Results]** to show the 4 winners advancing to Round 2

### 🏆 Round 2: The Semi-Finals (4 Players → 2 Winners)

Round 2 consists of **2 simultaneous matches** where the Round 1 winners compete:

#### 🎯 Match Structure in Round 2

- **Match 1**: Round 1 Winner A vs Round 1 Winner B
- **Match 2**: Round 1 Winner C vs Round 1 Winner D

#### 🔄 Player Client Behavior

- Player clients check if they advanced from Round 1
- If a player is not a winner, their client stops/exits
- Winners from Round 1 continue to Round 2

#### 🎲 Best-of-3 Series Process for Round 2

1. Click **[Start Round 2]** button to begin Round 2
2. Follow the same best-of-3 process as Round 1 for Match 1
3. Follow the same best-of-3 process as Round 1 for Match 2
4. The 2 match winners advance to the finals (Round 3)

### 🏅 Round 3: The Championship Final (2 Players → 1 Champion)

Round 3 consists of **1 final match** between the 2 remaining players:

#### 🎯 Match Structure in Round 3

- **Championship Match**: Round 2 Winner 1 vs Round 2 Winner 2

#### 🎲 Best-of-3 Championship Series

1. Click **[Start Round 3]** button to begin the final round
2. Follow the same best-of-3 process as previous rounds
3. The winner of this final match becomes the tournament champion
4. The champion should be displayed prominently at the end of Round 3

### 📊 Match Results Summary

- **Round 1**: 4 matches × 3 games each = up to 12 individual games
- **Round 2**: 2 matches × 3 games each = up to 6 individual games  
- **Round 3**: 1 match × 3 games = up to 3 individual games
- **Total**: Up to 21 individual Rock-Paper-Scissors games per tournament



### 🎲 Official Game Rules

**The Sacred Laws of Rock-Paper-Scissors:**

- 🪨 **Rock** crushes ✂️ **Scissors**
- 📄 **Paper** covers 🪨 **Rock**  
- ✂️ **Scissors** cuts 📄 **Paper**

**Move Values:**
- `1` = Rock (🪨)
- `2` = Paper (📄)
- `3` = Scissors (✂️)

**Victory Conditions:**
- Win your match → Advance to next round
- Lose your match → Tournament ends (but honor remains!)
- Tie → System handles resolution (typically rematch)

## 🎮 Round Management System

### 🎬 The Round Lifecycle

Each round follows a carefully orchestrated sequence:

#### 🚦 Phase 1: Round Preparation
1. **Server Status**: Changes round status to "Preparing"
2. **Player Notification**: All eligible players notified of upcoming round
3. **Referee Control**: Tournament director prepares to start the round
4. **Client Polling**: Clients continuously check for round status updates

#### 🏁 Phase 2: Round Start
1. **Referee Action**: Clicks the "Start Round" button in the web interface
2. **Server Response**: 
   - Updates round status to "In Progress"
   - Creates match pairings for current round
   - Notifies all clients via SignalR
3. **Client Detection**: Clients detect the status change through polling
4. **Player Activation**: Players can now submit their moves

#### ⚡ Phase 3: Move Submission
1. **Player Decision**: Each player chooses Rock, Paper, or Scissors
2. **API Call**: Client submits move via secure API endpoint
3. **Server Processing**: 
   - Validates move submission
   - Records move in database
   - Updates match status
4. **Privacy Protection**: Web UI shows "Move Submitted ✓" but hides actual choice
5. **Progress Tracking**: System tracks completion percentage

#### 🎊 Phase 4: Round Resolution
1. **Completion Check**: Server verifies all players have submitted moves
2. **Referee Control**: Tournament director clicks "Show Results" button
3. **Winner Calculation**: Server applies RPS rules to determine match winners
4. **Result Broadcast**: Results revealed simultaneously to all participants
5. **Advancement**: Winners automatically moved to next round bracket

#### 🔄 Phase 5: Round Transition
1. **Status Update**: Server changes to "Round Complete"
2. **Next Round Prep**: System automatically sets up next round bracket
3. **Player Filtering**: Only winners remain active for next round
4. **Cycle Restart**: Process repeats until champion is crowned

### 🎛️ Referee Controls Dashboard

The referee web interface provides complete tournament control:

#### 🖥️ Main Dashboard Features

**Tournament Status Panel:**
- Real-time player count (X/8)
- Current round indicator
- Tournament phase status
- Live match progress

**Control Buttons:**
- 🟢 **Start Round**: Initiates the next tournament round
- 🔍 **Show Results**: Reveals round outcomes to all players
- 📊 **Tournament Stats**: Displays comprehensive statistics
- 🔄 **Reset Tournament**: Emergency tournament restart

**Live Match Monitoring:**
- Player move submission status
- Match completion progress
- Real-time bracket updates
- Player elimination tracking

#### 🎯 Referee Decision Points

**When to Start a Round:**
- All players from previous round are ready
- System shows "Ready to Start Round X"
- Appropriate time interval has passed
- All participants are present and active

**When to Show Results:**
- 100% move submission completion
- All matches in current round finished
- Appropriate suspense timing
- Fair revelation to all players simultaneously

