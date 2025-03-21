from abc import ABC, abstractmethod
from typing import Optional

from src.model.board import Board
from src.model.hand import Hand


class BaseChooseRowStrategy(ABC):
    @abstractmethod
    def choose_row(self, hand: Optional[Hand] = None, board: Optional[Board] = None) -> int:
        pass

    def update(self, reward: float) -> None:
        return
