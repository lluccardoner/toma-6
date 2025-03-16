from random import Random

from src.model.board import BOARD_ROWS
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class RandomChooseRowStrategy(BaseChooseRowStrategy):
    def __init__(self, seed: int = None):
        self.randomizer = Random(seed)

    def choose_row(self) -> int:
        return self.randomizer.randint(0, BOARD_ROWS - 1)
