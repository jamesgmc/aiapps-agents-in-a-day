
this is the Paper Scissors Rock Game server


the game server should have a web frontend showing the game state in a tournament style/display
8 teams in each tournament

all the backend actions are exposed as REST APIs for the game clients

the process of the game is as follows:
1. client calls api to register a player
2. players are assigned into tournament and give a unique player number
3. for each round, players call api to submit their move (rock, paper, or scissors)
4. the server determines the winner of each match based on the rules of rock-paper-scissors
5. the server updates the game state and notifies players of the results
6. next round begins with the winners of the previous round

the server should have:
1- server side restful api
2- web frontend to display the game state on server side

all games server code should be placed in the `apps/psr-game-server` directory.
the web frontend should be built using React





