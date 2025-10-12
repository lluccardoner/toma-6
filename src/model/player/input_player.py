from src.model.player.base_player import BasePlayer
from src.model.strategy.choose_card.input_choose_card_strategy import InputChooseCardStrategy
from src.model.strategy.choose_row.input_choose_row_strategy import InputChooseRowStrategy


class InputPlayer(BasePlayer):
    def __init__(self, name: str):
        super().__init__(
            name=name,
            choose_card_strategy=InputChooseCardStrategy(),
            choose_row_strategy=InputChooseRowStrategy()
        )

    def copy(self) -> "InputPlayer":
        return InputPlayer(name=self.name)
