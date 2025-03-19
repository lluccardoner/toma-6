# Toma 6 simulations

## Table of Contents

- [What is Toma 6?](#what-is-toma-6)
- [Game config](#game-config)
- [Game](#game)
- [Simulation](#simulation)
- [Players](#players)
    - [Random player](#random-player)

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
Each game config has:

- A unique id
- A descriptive name
- A set of players with each player type and name

The config naming convention
is: `{id}-{player_type_1}_{player_type_1_num_players}-...-{player_type_N}_{player_type_N_num_players}`

## Game

A game is run based on a game config.

You can run a test game with 2 random players:

```bash
python main_game.py --seed 42
```

You can run a game with a wanted config:

```bash
python main_game.py --config "2-random_10.json" --seed 42
```

## Simulation

A simulation is basically repeating a game N times and see who wins each time.
The difference between games within a simulation is the seed for the randomisation.

Run a simulation:

```bash
python main_simulation.py --seed 42
```

Or you can specify the number of games to run for and the different game configs to try:

```bash
python main_simulation.py --seed 42 --num-games 10 --config "1-random_2.json" "2-random_10.json"
```

## Players

Here comes the fun part. The idea is to code different types of players and see which one wins more games.
The most basic player has a random strategy when playing a card or when choosing to take a row.
See implementations on `src/model/player`.

The `BasePlayer` class is the parent class of all players.
The two decisions of a player during the game are:

- Choose a card to play each turn
- Chose a row to take if you played the 6th card or if you played a low card that can not be placed

### Random player

`type="random"`

The random player is the most basic player that always make random decisions when playing a card or choosing a row to
take.

- Choose a card: chooses a random card from the hand
- Choose a row to take: chooses a random row to take

# TODO
- Add in README how to create player and strategy
- Create hand class (str, rpr and draw card from value)
- Create board row class
- Add player types in README
- Add results
- Add game configs with new choose row strategy
- Add strategies in simulation results