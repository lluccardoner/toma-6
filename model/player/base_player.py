import abc
from abc import ABC
from typing import List

from model.card import Card


class BasePlayer(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.hand: List[Card] = []
        self.total_points: int = 0
        self.round_points: List[int] = []

    @abc.abstractmethod
    def choose_card(self) -> Card:
        pass

    @abc.abstractmethod
    def choose_row(self) -> Card:
        pass

    def reset_hand(self):
        self.hand = []

    def reset_points(self):
        self.total_points = 0
        self.round_points = []
