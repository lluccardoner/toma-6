from abc import ABC
from typing import List

from src.model.card import Card
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class BasePlayer(ABC):
    def __init__(self,
                 name: str,
                 choose_card_strategy: BaseChooseCardStrategy,
                 choose_row_strategy: BaseChooseRowStrategy
                 ):
        self.name: str = name
        self.hand: List[Card] = []
        self.total_points: int = 0
        self.round_points: List[int] = []
        self.choose_card_strategy = choose_card_strategy
        self.choose_row_strategy = choose_row_strategy

    def choose_card(self) -> Card:
        return self.choose_card_strategy.choose_card(self.hand)

    def choose_row(self) -> int:
        return self.choose_row_strategy.choose_row()

    def reset_hand(self):
        self.hand = []

    def reset_points(self):
        self.total_points = 0
        self.round_points = []
