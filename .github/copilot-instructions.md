

## PSR Game Process

1- open #file:apps/psr-game-server in dotnet, and make sure the frontend webpage is accessable
2- use #file:apps/apps/psr-game-client/main.py to simulate 8 players in the game, the clients should all be able register themself
3- once all 8 players are registered, psr-game-server's web page should be ready to start the round. [Start Match] should be enabled
4- click [Start Match] button to start first match. also click [Start Match Round] button to start first match round
5- once [Start Match Round] button is clicked, the players can send their results for the match round.
6- when all players have sent their result, the [Release Round Results] button should be enabled. click [Release Round Results] will display the winners of the round.
7- repeat [Start Match Round] for 3 times, whoever wins most is the winner of the match.
8- once all 3 rounds are played, [Release Match Results] button should be enabled. click [Release Match Results] will show all the winners of the match
9- the player clients need to know if they are going into next match of the tournament. if they are not winner, just stop the client
10- for the winners of first match, they will go into the second match of the tournament.
11- click [Start Match] button to start second match. also click [Start Match Round] button to start first match round in second match. repeat step 5, step 6, step 7, step 8, step 9, step 10 for the second match of the tournament.
12- finally, for the third of tournament, repeat the same process.
13- when all 3 matches completes, the winner should be displayed.

