from typing import Optional

from src.model.typing import ChosenCardsHistoryType
from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy


class InputChooseCardStrategy(BaseChooseCardStrategy):

    def choose_card(
            self,
            hand: Hand,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None,
            chosen_cards_history: Optional[ChosenCardsHistoryType] = None
    ) -> Card:
        card_value = int(input(f"Choose a card of your hand: {hand!s} -> "))
        return hand.pop_card_by_value(card_value)
