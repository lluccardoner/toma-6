import os
import uuid
from datetime import datetime
from typing import Optional, List

import numpy as np

from src.controller.controller import GameController
from src.logger import get_simulation_logger, LoggingMode
from src.model.game_config import GameConfig
from src.model.game_config import PlayerType
from src.model.player.player_factory import PlayerFactory
from src.model.player.rl_evolution_strategy.rl_es_player import RLEvolutionStrategyPlayer

LOG_GAME_SAMPLER = 100

RESULTS_FOLDER = "results/"


# TODO maybe subclass of simulation?
class EvolutionStrategy:
    def __init__(self, game_config: GameConfig, num_games: int = 100, seed: Optional[int] = None):
        self.logger = get_simulation_logger()
        self.seed = seed
        self.randomizer = np.random.default_rng(seed)
        self.simulation_id = str(uuid.uuid4())
        self.date_time = datetime.now()

        self.output_path = os.path.join(RESULTS_FOLDER, self.simulation_id)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.game_config = game_config
        self.num_games = num_games

    def run(self, population_size: int, sigma: float, lr: float):
        self.logger.info(f"Running simulation id={self.simulation_id} for game_id={self.game_config.game_id}")
        logger_file = os.path.join(self.output_path, "game-sample.log")
        seeds: List[int] = self.randomizer.integers(low=1, high=self.num_games * 100, size=self.num_games).tolist()

        # Players are the same throughout the simulation
        other_players = [
            PlayerFactory.create_player(player_config, seed=self.seed)
            for player_config
            in self.game_config.players
            if player_config.player_type != PlayerType.RL_ES_LEARNER
        ]

        rl_es_players = [
            PlayerFactory.create_player(player_config, seed=self.seed)
            for player_config
            in self.game_config.players
            if player_config.player_type == PlayerType.RL_ES_LEARNER
        ]

        assert len(rl_es_players) == 1, "Expected exactly one RLEvolutionStrategyPlayer in players"

        # This is the player that will evolve
        rl_es_player: RLEvolutionStrategyPlayer = rl_es_players[0]

        num_params = len(rl_es_player.get_policy_nn().get_params())

        self.logger.info(f"Evolution Strategy parameters: {population_size=}, {sigma=}, {lr=}, {num_params=}")

        for game_number, game_seed in enumerate(seeds):
            t0 = datetime.now()

            logging_mode = LoggingMode.TO_FILE_SILENT
            if game_number == 0 or game_number % LOG_GAME_SAMPLER == 0:
                self.logger.info(f"Running simulation {game_number} of {self.num_games}")
                logging_mode = LoggingMode.TO_FILE_VERBOSE  # Only log a sample of games

            # Random noise for mutation for each member of the population
            N = self.randomizer.standard_normal(size=(population_size, num_params))

            # Rewards for each mutation in the population
            R = np.zeros(population_size)

            # TODO parallelize over population
            for j in range(population_size):
                rl_es_player_try = rl_es_player.mutate(sigma * N[j])  # Creates a new player with mutated params
                game_players = other_players + [rl_es_player_try]
                game = GameController(game_players, seed=game_seed, logging_mode=logging_mode, logger_file=logger_file)
                winner = game.play()
                # TODO try with different reward formulas
                if winner == rl_es_player_try:
                    R[j] = 1
                else:
                    R[j] = -rl_es_player_try.total_points

            m = R.mean()
            s = R.std()
            if s == 0:
                # we can't apply the following equation
                # self.logger.info(f"Iter: {game_number}, skipping update due to zero stddev")
                # TODO early stopping?
                continue

            A = (R - m) / s  # Normalize rewards to have std 1 and mean 0

            params_update = lr / (population_size * sigma) * np.dot(N.T, A)
            rl_es_player.update(params_update)

            lr *= 0.992354

            self.logger.info(
                f"Iter: {game_number}, "
                f"Avg reward: {m:.3f}, "
                f"Max reward: {R.max()}, "
                f"LR: {lr}, "
                f"Duration: {datetime.now() - t0}"
            )

        rl_es_player.save_policy(self.output_path)
        self.logger.info(f"Finished simulation id={self.simulation_id} for game_id={self.game_config.game_id}")
