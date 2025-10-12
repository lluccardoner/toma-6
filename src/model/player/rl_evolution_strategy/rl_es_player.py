import os
from typing import Optional

import numpy as np

from src.model.player.base_player import BasePlayer
from src.model.player.rl_evolution_strategy.nn import ANN
from src.model.strategy.choose_card.rl_es_choose_card_strategy import (
    RLEvolutionStrategyChooseCardStrategy
)
from src.model.strategy.choose_row.min_points_choose_row_strategy import MinPointsChooseRowStrategy


class RLEvolutionStrategyPlayer(BasePlayer):
    def __init__(self, name: str, policy_nn: Optional[ANN] = None):
        super().__init__(
            name=name,
            choose_card_strategy=RLEvolutionStrategyChooseCardStrategy(policy_nn),
            choose_row_strategy=MinPointsChooseRowStrategy()
        )

    @property
    def policy_nn(self) -> ANN:
        return self.choose_card_strategy.policy_nn

    def mutate(self, mutation: np.ndarray) -> "RLEvolutionStrategyPlayer":
        mutated_policy_nn = self.policy_nn.mutate(mutation)
        # Return a new player with the mutated policy instead of modifying in place
        mutated_player = RLEvolutionStrategyPlayer(self.name, mutated_policy_nn)
        return mutated_player

    def update(self, update: np.ndarray) -> None:
        self.policy_nn.update(update)

    def save_policy(self, output_path: str) -> None:
        output_file = os.path.join(output_path, f"nn_{self.name}.npz")
        nn = self.policy_nn
        nn.save(output_file)

    @classmethod
    def load(cls, player_name: str, file_path: str) -> "RLEvolutionStrategyPlayer":
        nn = ANN.load(file_path)
        player = cls(name=player_name, policy_nn=nn)
        return player

    def copy(self) -> "RLEvolutionStrategyPlayer":
        return RLEvolutionStrategyPlayer(self.name, self.policy_nn.copy())
