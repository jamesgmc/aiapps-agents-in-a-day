
# Ready

:::info

Ask for help if you are not sure what to do. If you are not technical, you can still join the game with a hosted game client.

:::


## Join with a Game Client

The game client is an AI App that is written in Node.js.

- Go to `apps-rps\rps-game-client` folder and run the following command to install dependencies:

```bash
npm install
```

- Once dependencies are installed, run the following command to start the game client:

```bash
npm run start
```

- Edit the game server urls in this file and replace url with your game server url if needed.

```
https://aiaaa-s2-game-server.azurewebsites.net/
```

- The game client will start on http://localhost:3000

![alt text](images\image-1.png)

- Type your player name and click "Register" to connect to the game server that is hosted on Azure.

![alt text](images\image-10.png)

- You are ready to play the game! Keep a record of the player ID that is assigned to you, you can use this ID to reconnect if your client disconnects.

## Join with a Game Agent

The game agent is an AI Agent that is written in python.

Go to `apps-rps\rps-game-agent` folder and run the following command to install dependencies:

```bash
pip install -r requirements.txt
```

- Once dependencies are installed, run the following command to start the game client:

```bash
python python .\app.py
```

- Edit the game server urls in this file and replace url with your game server url if needed. Check your local .env file and update the following variables:

```
https://aiaaa-s2-game-server.azurewebsites.net/
```

- The game client will start on http://localhost:5001. Go to browser and open the url.

![alt text](images\image-3.png)

- Type your player name and click "Register" to connect to the game server that is hosted on Azure.

![alt text](images\image-4.png)

- You are ready to play the game! Keep a record of the player ID that is assigned to you, you can use this ID to reconnect if your client disconnects.


