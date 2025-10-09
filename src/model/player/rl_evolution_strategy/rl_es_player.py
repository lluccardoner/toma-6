from typing import Optional

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
