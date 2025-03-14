# Toma 6 simulations

## What is Toma 6?
[Toma 6](https://en.wikipedia.org/wiki/6_nimmt!) is a card game for 2–10 players. 
The game has 104 cards, each bearing a number and one to seven bull's heads symbols that represent penalty points. 
A round of ten turns is played where all players place one card of their choice onto the table. 
The placed cards are arranged on four rows according to fixed rules. 
If placed onto a row that already has five cards then the player receives those five cards, 
which count as penalty points that are totaled up at the end of the round. 
Rounds are played until a player reaches 66 points, whereupon the player with the least penalty points wins.

Note: current implementation is 4 rounds instead of reaching 66 points.

## Game config
Under the `config` folder, different game configs can be defined.
Each game config has a unique id, a name and a set of players with each player type and name.

## Game
A game is run based on a game config.

You can run a test game with 2 random players:
```bash
python main_game.py --seed 42
```

You can run a game with a wanted config:
```bash
python main_game.py --config "2_random_10.json" --seed 42
```

## Simulation
A simulation is basically repeating a game N times and see who wins each time. 
The difference between games within a simulation is the seed for the randomisation.

Run a simulation:
```bash
python main_simulation.py 
```

## Players
Here comes the fun part. The idea is to code different types of players and see which one wins more games.
The most basic player has a random strategy when playing a card or when choosing to take a row.
See implementations on `src/model/player`.