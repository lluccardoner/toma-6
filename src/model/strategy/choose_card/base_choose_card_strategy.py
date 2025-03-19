import abc
from typing import List, Optional

from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand


class BaseChooseCardStrategy(abc.ABC):
    @abc.abstractmethod
    def choose_card(self, hand: Hand, board: Optional[Board] = None) -> Card:
        pass
