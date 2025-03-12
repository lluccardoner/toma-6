from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.controller.controller import GameController
from src.model.game_config import GameConfig

from random import Random

MAX_SEED = 1_000_000

class Simulation:
    def __init__(self, game_config: GameConfig, num_games: int = 100, seed: Optional[int] = None):
        self.seed = seed
        self.randomizer = Random(seed)

        self.game_config = game_config
        self.num_games = num_games
        self.results = pd.DataFrame(columns=[
            "game_id", "game_name", "game_number", "game_seed",
            "player_name", "player_class", "total_points",
            "round_1_points", "round_2_points", "round_3_points", "round_4_points"
        ])

    def run(self):
        seeds = [self.randomizer.randint(1, MAX_SEED) for _ in range(self.num_games)]
        for game_number, game_seed in enumerate(seeds):
            game = GameController(self.game_config, seed=game_seed)
            winner = game.play()

            game_results = pd.DataFrame(
                [
                    {
                        "game_id": self.game_config.game_id,
                        "game_name": self.game_config.name,
                        "game_number": game_number,
                        "game_seed": game_seed,
                        "player_name": player.name,
                        "player_class": player.__class__.__name__,
                        "is_winner": player.name == winner.name,
                        "total_points": player.total_points,
                        "round_1_points": player.round_points[0],
                        "round_2_points": player.round_points[1],
                        "round_3_points": player.round_points[2],
                        "round_4_points": player.round_points[3],
                    }
                    for player in game.players
                ]
            )

            self.results = pd.concat([self.results, game_results], ignore_index=True)

        self.plot_results()

    def plot_results(self):
        plt.figure(figsize=(12, 6))
        sns.violinplot(
            data=self.results,
            x="player_name",
            y="total_points",
            inner=None,  # Hide inner box plot
            scale="width",
            linewidth=1,
            alpha=0.7
        )

        """
        sns.scatterplot(
            data=self.results,
            x="player_name",
            y="total_points",
            hue="is_winner",
            palette={True: "red", False: "black"},
            style="is_winner",
            markers={True: "o", False: "X"},
            s=60,  # Adjust marker size
            edgecolor="black"
        )
        """

        plt.title("Total Points per Player Across Games")
        plt.xlabel("Player Name")
        plt.ylabel("Total Points")
        plt.xticks(rotation=45)
        plt.legend(title="Winner", labels=["Loser", "Winner"], loc="upper right")
        plt.grid(True, linestyle="--", alpha=0.5)

        plt.show()
