

## PSR Game Process

# Starting game
- run server side here #file:apps/psr-game-server in dotnet, and make sure the frontend webpage is accessable
- run #file:apps/psr-game-client/main.py multiple times to simulate 4 players in the game, the clients should all be able register themselves to the tournament
- once all 4 players are registered, psr-game-server's web page should be ready to start the round. [Start Round] button should be enabled.

# Round 1
- click [Start Round 1] button to start Round 1. [Start Match] button should be enabled. 
- then click [Start Match] button to start Match 1 in the Round 1
- once [Start Match] button is clicked, the players can send their results for Match 1.
- when all players have sent their results, the [Release Match Results] button should be enabled. 
- click [Release Match Results] will then display the winners of the match.

## Match 2 and Match 3 in Round 1
- repeat the same process for Match 2 and Match 3 in Round 1
- whoever wins most is the winner of the round.
- once all 3 matches are played, [Release Round Results] button should be enabled. 
- click [Release Round Results] will show all the winners of the round

# Round 2
- the player clients need to know if they are going into next round of the tournament. if they are not winner, just stop the client
- for the winners of Round 1, they will go into the Round 2 of the tournament.
- click [Start Round 2] button to start Round 2. 
- click [Start Match] button to start Match 1 in Round 2. 
- repeat the steps in Round 1 for all 3 matches in Round 2
- the winners of Round 2 will go into the final of the tournament.

# Round 3
- for Round 3, repeat the same process for rounds and games.
- the winner should be displayed in the end of round 3.

