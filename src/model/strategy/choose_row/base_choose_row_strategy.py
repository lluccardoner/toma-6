import abc
from typing import Optional, List

from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand


class BaseChooseRowStrategy(abc.ABC):
    @abc.abstractmethod
    def choose_row(self, hand: Optional[Hand] = None, board: Optional[Board] = None) -> int:
        pass
