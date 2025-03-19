from typing import Optional

from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy


class LevelChooseCardStrategy(BaseChooseCardStrategy):
    def __init__(self, level: float):
        # Level 0: pick always lowest card
        # Level 1: pick always highest card
        assert 0 <= level <= 1, "Level must be between 0 <= level <= 1"
        self.level = level

    def choose_card(self, hand: Hand, board: Optional[Board] = None) -> Card:
        # Hand is always sorted from low to high
        card_index = int((len(hand) - 1) * self.level)
        return hand.pop_card_by_index(card_index)


class MinChooseCardStrategy(LevelChooseCardStrategy):
    def __init__(self):
        super().__init__(level=0)


class MidChooseCardStrategy(LevelChooseCardStrategy):
    def __init__(self):
        super().__init__(level=0.5)


class MaxChooseCardStrategy(LevelChooseCardStrategy):
    def __init__(self):
        super().__init__(level=1)
