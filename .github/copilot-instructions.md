
the game server should have a asp.net web frontend showing the game state in a tournament style/display.
all games server code should be placed in the apps-rps/rps-game-server directory.

all the backend actions are exposed as REST APIs for the game clients (you dont need to implement client)

the process of the game is as follows:
1- each client calls api to register a player
2- players are assigned into tournament and give a unique player number
4- the server determines the winner of each round
5- the server updates the game state and notifies players of the results

the process of the round is follow
1- there are 5 rounds in total, the tournament status is Pending
2- the referee will start the tournament by clicked [Start Tournament] button
3- each players will see the tournament status as InProgress, and round 1 status as Pending.
4- the referee will start the round by clicked [Start Round] button, server side will decide on [Paper, Scissors, Rock] and keep it hidden, also give a match question for the player to resolve
5- each player will see the round status as InProgress in api and able to pull the question of the round
6- each player will try to resolve the question, then they will submit the answer and their move (rock, paper, or scissors)
7- the website should show how many players are in the round and if they have submiited answer and move
8- the referee will end the round by clicking [End Round] button. each player's result will be displayed and a score calculated and summed for each play. a leader board will be shown to see how is having highest scores.
9- continue the same process and repeat for 5 times.
10- for the last 2 rounds, do not show the leaderboard and keep result hidden.
11- after last round, the referee will click [End Tournament] to display current top 3 winners and everyone's score.
12- create a grid page to display the results of each player's each round for each tracing

the server should have:
1- web to display the game state
2- server side restful api

