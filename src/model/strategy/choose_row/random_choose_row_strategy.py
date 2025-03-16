from random import Random
from typing import Optional, List

from src.model.board import BOARD_ROWS, Board
from src.model.card import Card
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class RandomChooseRowStrategy(BaseChooseRowStrategy):
    def __init__(self, seed: int = None):
        self.randomizer = Random(seed)

    def choose_row(self, hand: Optional[List[Card]] = None, board: Optional[Board] = None) -> int:
        return self.randomizer.randint(0, BOARD_ROWS - 1)
