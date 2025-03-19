from typing import List

from src.model.card import Card


class Hand:
    def __init__(self):
        self.cards: List[Card] = []

    def __str__(self):
        return str([card.value for card in self.cards])

    def __repr__(self):
        return f"Hand({self!s})"

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def reset(self):
        self.cards = []

    def sort(self):
        self.cards.sort(key=lambda card: card.value)

    def add_card(self, card: Card):
        self.cards.append(card)

    def pop_card_by_value(self, card_value: int) -> Card:
        card_index = next(i for i, card in enumerate(self.cards) if card.value == card_value)
        return self.pop_card_by_index(card_index)

    def pop_card_by_index(self, index: int) -> Card:
        return self.cards.pop(index)
