import abc
from typing import List, Optional

from src.model.board import Board
from src.model.card import Card


class BaseChooseCardStrategy(abc.ABC):
    @abc.abstractmethod
    def choose_card(self, hand: List[Card], board: Optional[Board] = None) -> Card:
        pass
