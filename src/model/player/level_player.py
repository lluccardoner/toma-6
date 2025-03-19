from src.model.player.base_player import BasePlayer
from src.model.strategy.choose_card.level_choose_card_strategy import LevelChooseCardStrategy
from src.model.strategy.choose_row.min_points_choose_row_strategy import MinPointsChooseRowStrategy


class LevelPlayer(BasePlayer):
    def __init__(self, name: str, level: float):
        super().__init__(
            name=name,
            choose_card_strategy=LevelChooseCardStrategy(level),
            choose_row_strategy=MinPointsChooseRowStrategy()
        )


class MinPlayer(LevelPlayer):
    def __init__(self, name: str):
        super().__init__(name, level=0)


class MidPlayer(LevelPlayer):
    def __init__(self, name: str):
        super().__init__(name, level=0.5)


class MaxPlayer(LevelPlayer):
    def __init__(self, name: str):
        super().__init__(name, level=1)
