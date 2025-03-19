from abc import ABC
from typing import List, Optional

from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class BasePlayer(ABC):
    def __init__(self,
                 name: str,
                 choose_card_strategy: BaseChooseCardStrategy,
                 choose_row_strategy: BaseChooseRowStrategy
                 ):
        self.name: str = name
        self.hand: Hand = Hand()
        self.total_points: int = 0
        self.round_points: List[int] = []
        self.choose_card_strategy = choose_card_strategy
        self.choose_row_strategy = choose_row_strategy

    def choose_card(self, board: Optional[Board] = None) -> Card:
        return self.choose_card_strategy.choose_card(hand=self.hand, board=board)

    def choose_row(self, board: Optional[Board] = None) -> int:
        return self.choose_row_strategy.choose_row(hand=self.hand, board=board)

    def sort_hand(self):
        self.hand.sort()

    def reset_hand(self):
        self.hand.reset()

    def reset_points(self):
        self.total_points = 0
        self.round_points = []
