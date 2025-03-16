from typing import List, Optional

from src.model.board import Board
from src.model.card import Card
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy


class InputChooseCardStrategy(BaseChooseCardStrategy):

    def choose_card(self, hand: List[Card], board: Optional[Board] = None) -> Card:
        card_value = int(input(f"Choose a card of your hand: {[card.value for card in hand]} -> "))
        choose_card = [i for i, card in enumerate(hand) if card.value == card_value][0]
        return hand.pop(choose_card)
