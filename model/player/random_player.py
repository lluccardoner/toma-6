import random

from model.board import BOARD_ROWS
from model.card import Card
from model.player.base_player import BasePlayer


class RandomPlayer(BasePlayer):
    def __init__(self, name):
        super().__init__(name)

    def choose_card(self) -> Card:
        return self.hand.pop(random.randint(0, len(self.hand) - 1))

    def choose_row(self) -> int:
        return random.randint(0, BOARD_ROWS - 1)
