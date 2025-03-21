from abc import ABC, abstractmethod
from typing import Optional

from src.model.typing import ChosenCardsHistoryType
from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand


class BaseChooseCardStrategy(ABC):
    @abstractmethod
    def choose_card(
            self,
            hand: Hand,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None,
            chosen_cards_history: Optional[ChosenCardsHistoryType] = None
    ) -> Card:
        pass

    def update(self, reward: float) -> None:
        # Update the strategy with the reward obtained
        return
