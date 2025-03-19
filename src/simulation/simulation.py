import os
import uuid
from datetime import datetime
from random import Random
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.controller.controller import GameController
from src.logger import get_simulation_logger, LoggingMode
from src.model.game_config import GameConfig

LOG_GAME_SAMPLER = 100

RESULTS_FOLDER = "results/"


class Simulation:
    def __init__(self, game_config: GameConfig, num_games: int = 100, seed: Optional[int] = None):
        self.logger = get_simulation_logger()
        self.seed = seed
        self.randomizer = Random(seed)
        self.simulation_id = str(uuid.uuid4())
        self.date_time = datetime.now()

        self.output_path = os.path.join(RESULTS_FOLDER, self.simulation_id)
        if not os.path.exists(self.output_path):
            os.mkdir(self.output_path)

        self.game_config = game_config
        self.num_games = num_games
        self.results = pd.DataFrame()

    def run(self):
        self.logger.info(f"Running simulation id={self.simulation_id} for game_id={self.game_config.game_id}")
        logger_file = os.path.join(self.output_path, "game-sample.log")
        seeds = [self.randomizer.randint(1, self.num_games * 100) for _ in range(self.num_games)]
        for game_number, game_seed in enumerate(seeds):
            logging_mode = LoggingMode.TO_FILE_SILENT
            if game_number == 0 or game_number % LOG_GAME_SAMPLER == 0:
                self.logger.info(f"Running simulation {game_number} of {self.num_games}")
                logging_mode = LoggingMode.TO_FILE_VERBOSE  # Only log a sample of games
            game = GameController(self.game_config, seed=game_seed, logging_mode=logging_mode, logger_file=logger_file)
            winner = game.play()

            game_results = pd.DataFrame(
                [
                    {
                        "simulation_id": self.simulation_id,
                        "simulation_seed": self.seed,
                        "simulation_date_time": self.date_time,
                        "simulation_num_games": self.num_games,
                        "game_id": self.game_config.game_id,
                        "game_name": self.game_config.name,
                        "game_number": game_number,
                        "game_seed": game_seed,
                        "player_name": player.name,
                        "player_class": player.__class__.__name__,
                        "player_choose_card_strategy": player.choose_card_strategy.__name__,
                        "player_choose_row_strategy": player.choose_row_strategy.__name__,
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

        self.save_results()
        self.plot_results()
        self.logger.info(f"Finished simulation id={self.simulation_id} for game_id={self.game_config.game_id}")

    def save_results(self):
        self.results.to_csv(os.path.join(self.output_path, "results.csv"), index=False)

    def plot_results(self):
        title = (
                f"Simulation \nid={self.simulation_id} seed={self.seed}" +
                f"\n Game \nid={self.game_config.game_id} num_games={self.num_games}"
        )

        self.plot_is_winner(title)
        if self.num_games <= 100:
            self.plot_swarm(title)
        self.plot_violin(title)
        self.plot_box(title)

    def plot_is_winner(self, title):
        plt.figure(figsize=(12, 6))
        sns.catplot(
            data=self.results,
            x="player_name",
            y="is_winner",
            kind="bar"
        )

        plt.title(title)
        plt.xlabel("Player Name")
        plt.ylabel("Is winner")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)

        plt.savefig(os.path.join(self.output_path, "is_winner.png"), dpi=300, bbox_inches="tight")

    def plot_swarm(self, title):
        plt.figure(figsize=(12, 6))
        sns.catplot(
            data=self.results,
            x="player_name",
            y="total_points",
            hue="is_winner",
            kind="swarm"
        )

        plt.title(title)
        plt.xlabel("Player Name")
        plt.ylabel("Total Points")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)

        plt.savefig(os.path.join(self.output_path, "swarm.png"), dpi=300, bbox_inches="tight")

    def plot_violin(self, title):
        plt.figure(figsize=(12, 6))
        sns.violinplot(
            data=self.results,
            x="player_name",
            y="total_points",
            hue="is_winner",
            split="true",
            inner="box",
            density_norm="count",
            linewidth=1,
            alpha=0.7,
        )

        plt.title(title)
        plt.xlabel("Player Name")
        plt.ylabel("Total Points")
        plt.xticks(rotation=45)
        plt.legend(title="Winner", labels=["Loser", "Winner"], loc="upper right")
        plt.grid(True, linestyle="--", alpha=0.5)

        plt.savefig(os.path.join(self.output_path, "violin.png"), dpi=300, bbox_inches="tight")

    def plot_box(self, title):
        plt.figure(figsize=(12, 6))
        sns.catplot(
            kind="box",
            data=self.results,
            x="player_name",
            y="total_points",
        )

        plt.title(title)
        plt.xlabel("Player Name")
        plt.ylabel("Total Points")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle="--", alpha=0.5)

        plt.savefig(os.path.join(self.output_path, "box.png"), dpi=300, bbox_inches="tight")
