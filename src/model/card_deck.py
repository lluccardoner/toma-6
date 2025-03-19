from random import Random
from typing import Optional

from src.model.card import Card

DECK_CARDS = [Card(i) for i in range(1, 105)]


class CardDeck:
    def __init__(self, seed: Optional[int] = None):
        self.randomizer = Random(seed)
        self.cards = DECK_CARDS.copy()
        self.shuffle()

    def reset_and_shuffle(self):
        self.reset()
        self.shuffle()

    def reset(self):
        self.cards = DECK_CARDS.copy()

    def shuffle(self):
        self.randomizer.shuffle(self.cards)
