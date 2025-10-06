from src.model.player.rl_q_value.rl_utils import QValueType
from src.model.player.base_player import BasePlayer
from src.model.strategy.choose_card.rl_choose_card_strategy import RLChooseCardStrategyLearner, RLChooseCardStrategy
from src.model.strategy.choose_row.min_points_choose_row_strategy import MinPointsChooseRowStrategy


class RLPlayerLearner(BasePlayer):
    def __init__(self, name: str, Q: QValueType = None):
        super().__init__(
            name=name,
            choose_card_strategy=RLChooseCardStrategyLearner(Q=Q),
            choose_row_strategy=MinPointsChooseRowStrategy()
        )

    def get_Q(self) -> QValueType:
        return self.choose_card_strategy.Q


class RLPlayer(BasePlayer):
    def __init__(self, name: str, Q: QValueType):
        super().__init__(
            name=name,
            choose_card_strategy=RLChooseCardStrategy(Q),
            choose_row_strategy=MinPointsChooseRowStrategy()
        )
