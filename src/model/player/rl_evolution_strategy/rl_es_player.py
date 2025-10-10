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

    def get_policy_nn(self) -> ANN:
        return self.choose_card_strategy.policy_nn

    def mutate(self, mutation: np.ndarray) -> "RLEvolutionStrategyPlayer":
        current_params = self.get_policy_nn().get_params()
        params_try = current_params + mutation
        mutated_player = RLEvolutionStrategyPlayer(self.name)
        mutated_player.get_policy_nn().set_params(params_try)
        return mutated_player

    def update(self, update: np.ndarray) -> None:
        current_params = self.get_policy_nn().get_params()
        new_params = current_params + update
        self.get_policy_nn().set_params(new_params)

    def save_policy(self, output_path):
        output_file = os.path.join(output_path, f"nn_{self.name}.npz")
        nn = self.get_policy_nn()
        nn.save(output_file)

    @classmethod
    def load(cls, player_name: str, file_path: str) -> "RLEvolutionStrategyPlayer":
        nn = ANN.load(file_path)
        player = cls(name=player_name, policy_nn=nn)
        return player
