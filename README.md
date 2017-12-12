# chain-reaction-game

The objective of Chain Reaction is to take control of the board by eliminating your opponents' orbs.

Players take it in turns to place their orbs in a cell. Once a cell has reached critical mass the orbs explode into the surrounding cells adding an extra orb and claiming the cell for the player. A player may only place their orbs in a blank cell or a cell that contains orbs of their own colour. As soon as a player looses all their orbs they are out of the game.

# Run Instructions 

This project utlizes 'web.py' python wsgi and mongodb, hence they are required to run this project. 
Terminal Commands:

1. mongod
2. python2.7 bin/app.py (this will start a local server at 0.0.0.0:8080

Now go to '0.0.0.0:8080/home' to start the game. 
