from typing import List, Optional

from src.model.card import Card

BOARD_ROWS = 4


class Board:
    def __init__(self):
        self.rows: List[List[Card]] = [[] for _ in range(BOARD_ROWS)]

    def reset(self):
        self.rows: List[List[Card]] = [[] for _ in range(BOARD_ROWS)]

    def get_points_per_row(self) -> List[int]:
        return [sum(card.points for card in row) for row in self.rows]

    def get_last_row_cards(self) -> List[Card]:
        return [row[-1] for row in self.rows if row]

    def find_valid_row(self, card: Card) -> Optional[int]:
        # Find the valid rows where the card can be played
        valid_rows = {
            idx: card.value - row[-1].value
            for idx, row in enumerate(self.rows)
            if card.value > row[-1].value
        }
        return min(valid_rows, key=valid_rows.get) if valid_rows else None
