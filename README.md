# Toma 6 simulations

![Tests](https://github.com/lluccardoner/toma-6/actions/workflows/test.yaml/badge.svg)

## Table of Contents

- [What is Toma 6?](#what-is-toma-6)
- [Game config](#game-config)
- [Game](#game)
- [Simulation](#simulation)
    - [Simulation output](#simulation-output)
- [Players](#players)
    - [Create a new Player](#create-a-new-player)
    - [Player types](#player-types)
- [Test](#test)

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

You can run a game with a given config:

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

### Simulation output

Each simulation has a unique ID. The simulation output is saved in the created simulation folder under `results`.
The output of a simulation is:

- `game-sample.log`: the game log of a sample of games. A game is logged every 100 games.
- `results.csv`: a pandas DataFrame in CSV format with the simulation results.
- `box.png`: a box plot of all the final points of the N games for each player (fewer points is better).
- `violin.png`: a violin plot of the distribution of final points per game fore each player. Split between won and lost
  games.
- `is_winner.png`: a bar plot of the percentage of games won by each player in the simulation.

## Players

Here comes the fun part. The idea is to code different types of players and see which one wins more games.
The most basic player has a random strategy when playing a card or when choosing to take a row.
See implementations on `src/model/player`.

The `BasePlayer` class is the parent class of all players.
The two decisions of a player during the game are:

- Choose a card to play each turn (see `BaseChooseCardStrategy`)
- Chose a row to take if you played the 6th card or if you played a low card that can not be placed (see
  `BaseChooseRowStrategy`)

### Create a new Player

To create a new player, you need to create a new class that inherits from `BasePlayer` and implement the abstract
methods. If you are creating a new strategy, you need to create a new class that inherits from `BaseChooseCardStrategy`
or `BaseChooseRowStrategy` and implement the abstract methods.

### Player types

| Player Type | Player Class   | Choose Card Strategy       | Choose Row Strategy          | Description                                                                                                                                                                                            |
|-------------|----------------|----------------------------|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `random`    | `RandomPlayer` | `RandomChooseCardStrategy` | `RandomChooseRowStrategy`    | The most basic player that always makes random decisions when playing a card or choosing a row to take. It randomly selects a card from its hand and randomly chooses a row when required to take one. |
| `input`     | `InputPlayer`  | `InputChooseCardStrategy`  | `InputChooseRowStrategy`     | A user input player. With this, you are able to play against the bot.                                                                                                                                  |
| `min`       | `MinPlayer`    | `MinChooseCardStrategy`    | `MinPointsChooseRowStrategy` | A player that always picks the card with the lowest value in its hand. When choosing a row, choose the row with less points.                                                                           |
| `mid`       | `MidPlayer`    | `MidChooseCardStrategy`    | `MinPointsChooseRowStrategy` | A player that always picks the card with the mid value in its hand. When choosing a row, choose the row with less points.                                                                              |
| `max`       | `MaxPlayer`    | `MaxChooseCardStrategy`    | `MinPointsChooseRowStrategy` | A player that always picks the card with the highest value in its hand. When choosing a row, choose the row with less points.                                                                          |

# Test

Run:

```bash
pytest
```

# TODO

- Add tests
    - GitHub actions and test pass check in README
    - Strategy tests
- Player config creation with strategy instead of player type?
- Add example simulation results
- Add game rules link
- What is needed for RL?
    - Add chose row history
