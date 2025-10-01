from src.model.player.base_player import BasePlayer
from src.model.strategy.choose_card.rl_choose_card_strategy import RLChooseCardStrategyLearner
from src.model.strategy.choose_row.min_points_choose_row_strategy import MinPointsChooseRowStrategy


class RLPlayerLearner(BasePlayer):
    def __init__(self, name: str):
        super().__init__(
            name=name,
            choose_card_strategy=RLChooseCardStrategyLearner(),
            choose_row_strategy=MinPointsChooseRowStrategy()
        )
