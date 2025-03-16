from typing import Optional, List

from src.model.board import Board
from src.model.card import Card
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class InputChooseRowStrategy(BaseChooseRowStrategy):

    def choose_row(self, hand: Optional[List[Card]] = None, board: Optional[Board] = None) -> int:
        row_points = ", ".join([f"Row {i + 1}: {p} points" for i, p in enumerate(board.get_points_per_row())])
        row_number = int(input(f"Choose a row number to take. {row_points} -> "))
        return row_number - 1
