from typing import List

from src.model.card import Card

BOARD_ROWS = 4


class Board:
    def __init__(self):
        self.rows: List[List[Card]] = [[] for _ in range(BOARD_ROWS)]

    def reset(self):
        self.rows: List[List[Card]] = [[] for _ in range(BOARD_ROWS)]
