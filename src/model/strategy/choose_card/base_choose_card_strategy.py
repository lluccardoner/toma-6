import abc
from typing import List

from src.model.card import Card


class BaseChooseCardStrategy(abc.ABC):
    @abc.abstractmethod
    def choose_card(self, hand: List[Card]) -> Card:
        pass
