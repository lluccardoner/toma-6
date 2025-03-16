from typing import Optional

from src.model.player.base_player import BasePlayer
from src.model.strategy.choose_card.random_choose_card_strategy import RandomChooseCardStrategy
from src.model.strategy.choose_row.random_choose_row_strategy import RandomChooseRowStrategy


class RandomPlayer(BasePlayer):
    def __init__(self, name: str, seed: Optional[int] = None):
        super().__init__(
            name=name,
            choose_card_strategy=RandomChooseCardStrategy(seed),
            choose_row_strategy=RandomChooseRowStrategy(seed)
        )
