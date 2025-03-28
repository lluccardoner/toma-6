from random import Random
from typing import Optional

from src.model.game_history import GameHistory
from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy


class RandomChooseCardStrategy(BaseChooseCardStrategy):
    def __init__(self, seed: int = None):
        self.randomizer = Random(seed)

    def choose_card(
            self,
            hand: Hand,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None,
            game_history: Optional[GameHistory] = None
    ) -> Card:
        card_index = self.randomizer.randint(0, len(hand) - 1)
        return hand.pop_card_by_index(card_index)
