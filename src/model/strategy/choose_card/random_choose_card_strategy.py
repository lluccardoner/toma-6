from random import Random
from typing import List, Optional

from src.model.board import Board
from src.model.card import Card
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy


class RandomChooseCardStrategy(BaseChooseCardStrategy):
    def __init__(self, seed: int = None):
        self.randomizer = Random(seed)

    def choose_card(self, hand: List[Card], board: Optional[Board] = None) -> Card:
        return hand.pop(self.randomizer.randint(0, len(hand) - 1))
