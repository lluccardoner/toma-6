import abc
from typing import Optional, List

from src.model.board import Board
from src.model.card import Card


class BaseChooseRowStrategy(abc.ABC):
    @abc.abstractmethod
    def choose_row(self, hand: Optional[List[Card]] = None, board: Optional[Board] = None) -> int:
        pass
