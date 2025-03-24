from abc import ABC, abstractmethod
from typing import Optional

from src.model.board import Board
from src.model.card import Card
from src.model.game_history import GameHistory
from src.model.hand import Hand


class BaseChooseCardStrategy(ABC):
    @abstractmethod
    def choose_card(
            self,
            hand: Hand,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None,
            game_history: Optional[GameHistory] = None
    ) -> Card:
        # Hand is always sorted from low to high
        pass

    def update(self, reward: float) -> None:
        # Update the strategy with the reward obtained
        return
