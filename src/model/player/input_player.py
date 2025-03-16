from typing import Optional

from src.model.player.base_player import BasePlayer
from src.model.strategy.choose_card.input_choose_card_strategy import InputChooseCardStrategy
from src.model.strategy.choose_card.random_choose_card_strategy import RandomChooseCardStrategy
from src.model.strategy.choose_row.input_choose_row_strategy import InputChooseRowStrategy
from src.model.strategy.choose_row.random_choose_row_strategy import RandomChooseRowStrategy


class InputPlayer(BasePlayer):
    def __init__(self, name: str):
        super().__init__(
            name=name,
            choose_card_strategy=InputChooseCardStrategy(),
            choose_row_strategy=InputChooseRowStrategy()
        )
