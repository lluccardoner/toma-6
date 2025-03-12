import abc
from abc import ABC
from random import Random
from typing import List, Optional

from src.model.card import Card


class BasePlayer(ABC):
    def __init__(self, name: str, seed: Optional[int] = None):
        self.randomizer = Random(seed)
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
