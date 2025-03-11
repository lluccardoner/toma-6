from random import Random
from typing import Optional

from model.card import Card

DECK_CARDS = [Card(i) for i in range(1, 105)]


class CardDeck:
    def __init__(self, seed: Optional[int] = None):
        self.seed = seed
        self.randomizer = Random(self.seed)
        self.cards = DECK_CARDS.copy()
        self.shuffle()

    def reset(self):
        self.cards = DECK_CARDS.copy()
        self.shuffle()

    def shuffle(self):
        self.randomizer.shuffle(self.cards)
