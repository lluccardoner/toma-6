from multiprocessing.dummy import Pool
from multiprocessing.pool import ThreadPool
from typing import Optional, List

import numpy as np
import pandas as pd

from src.model.player.base_player import BasePlayer
from src.controller.controller import GameController
from src.logger import LoggingMode
from src.model.game_config import GameConfig
from src.model.player.rl_evolution_strategy.rl_es_player import RLEvolutionStrategyPlayer
from src.simulation.simulation import Simulation

LOG_GAME_SAMPLER = 100

RESULTS_FOLDER = "results/"


class EvolutionStrategy(Simulation):
    def __init__(
            self,
            game_config: GameConfig,
            population_size: int = 50,
            sigma: float = 0.1,
            lr: float = 0.03,
            lr_decay: float = 0.992354,
            num_games: int = 100,
            seed: Optional[int] = None
    ):
        super().__init__(game_config, num_games, seed)

        self.population_size = population_size
        self.sigma = sigma
        self.lr = lr
        self.lr_decay = lr_decay

        self.pool: ThreadPool = Pool(8)

    def run(self):
        self.logger.info(f"Running evolution strategy id={self.simulation_id} for game_id={self.game_config.game_id}")
        logger_file = self.get_logger_file()
        seeds = self.get_game_seeds()
        players = self.get_players()  # Players are the same throughout the simulation

        # Players are the same throughout the simulation
        other_players = [
            player
            for player
            in players
            if not isinstance(player, RLEvolutionStrategyPlayer)
        ]

        rl_es_players = [
            player
            for player
            in players
            if isinstance(player, RLEvolutionStrategyPlayer)
        ]

        assert len(rl_es_players) == 1, "Expected exactly one RLEvolutionStrategyPlayer in players"

        # This is the player that will evolve
        rl_es_player: RLEvolutionStrategyPlayer = rl_es_players[0]

        for game_number, game_seed in enumerate(seeds):
            self.run_mutations(game_number, game_seed, other_players, rl_es_player)
            # Play a game with the best mutation
            game_results = self.play_game(game_number, game_seed, logger_file, players)
            self.results = pd.concat([self.results, game_results], ignore_index=True)

        self.is_winner_results = self.compute_winner_results()
        print(self.is_winner_results)
        self.save_results()
        self.plot_results()
        self.save_players_state(players)
        self.logger.info(f"Finished simulation id={self.simulation_id} for game_id={self.game_config.game_id}")

    def run_mutations(self, game_number, game_seed, other_players, rl_es_player):
        num_params = len(rl_es_player.policy_nn.get_params())
        # Random noise for mutation for each member of the population
        N = self.randomizer.standard_normal(size=(self.population_size, num_params))

        ## SLOW VERSION
        # R = np.zeros(self.population_size) # Rewards for each mutation in the population
        #
        # for j in range(self.population_size):
        #     rl_es_player_try = rl_es_player.mutate(self.sigma * N[j])  # Creates a new player with mutated params
        #     other_players_copy = [player.copy() for player in other_players] # Copy so they don't share state
        #     R[j] = self.get_reward(game_seed, other_players_copy, rl_es_player_try)

        ## FAST VERSION ??
        R = self.pool.starmap(
            self.get_reward,
            [
                (game_seed, [player.copy() for player in other_players], rl_es_player.mutate(self.sigma * N[j]))
                for j
                in range(self.population_size)
            ]
        )
        R = np.array(R)

        m = R.mean()
        s = R.std()
        if s != 0:
            A = (R - m) / s  # Normalize rewards to have std 1 and mean 0

            params_update = self.lr / (self.population_size * self.sigma) * np.dot(N.T, A)
            rl_es_player.update(params_update)

            self.lr *= self.lr_decay

        self.logger.info(
            f"Iter: {game_number}, "
            f"Avg reward: {m:.3f}, "
            f"Max reward: {R.max()}, "
            f"LR: {self.lr}"
        )

    def get_reward(self, game_seed: int, other_players: List[BasePlayer],
                   rl_es_player_try: RLEvolutionStrategyPlayer) -> int:
        evolution_game_players = other_players + [rl_es_player_try]
        evolution_game = GameController(evolution_game_players, seed=game_seed,
                                        logging_mode=LoggingMode.TO_CONSOLE_SILENT)
        evolution_winner = evolution_game.play()
        # Reward function
        if evolution_winner == rl_es_player_try:
            reward = 1
        else:
            reward = -rl_es_player_try.total_points

        return reward
