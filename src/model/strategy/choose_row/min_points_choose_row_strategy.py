from typing import Optional, List

from src.model.board import Board
from src.model.card import Card
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class MinPointsChooseRowStrategy(BaseChooseRowStrategy):

    def choose_row(self, hand: Optional[List[Card]] = None, board: Optional[Board] = None) -> int:
        row_points = board.get_points_per_row()
        return row_points.index(min(row_points))
