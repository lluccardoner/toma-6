from typing import List

from src.model.card import Card

BOARD_ROWS = 4


class Board:
    def __init__(self):
        self.rows: List[List[Card]] = [[] for _ in range(BOARD_ROWS)]

    def reset(self):
        self.rows: List[List[Card]] = [[] for _ in range(BOARD_ROWS)]

    def get_points_per_row(self) -> List[int]:
        return [sum(card.points for card in row) for row in self.rows]
