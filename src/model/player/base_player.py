from abc import ABC, abstractmethod
from typing import List, Optional

from src.model.board import Board
from src.model.card import Card
from src.model.game_history import GameHistory
from src.model.hand import Hand
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class BasePlayer(ABC):
    def __init__(self,
                 name: str,
                 choose_card_strategy: BaseChooseCardStrategy,
                 choose_row_strategy: BaseChooseRowStrategy
                 ):
        self.name: str = name
        self.hand: Hand = Hand()
        self.total_points: int = 0
        self.round_points: List[int] = []
        self.choose_card_strategy = choose_card_strategy
        self.choose_row_strategy = choose_row_strategy

    def choose_card(self,
                    board: Optional[Board] = None,
                    current_round: Optional[int] = None,
                    current_turn: Optional[int] = None,
                    game_history: Optional[GameHistory] = None) -> Card:
        return self.choose_card_strategy.choose_card(
            hand=self.hand,
            board=board,
            current_round=current_round,
            current_turn=current_turn,
            game_history=game_history
        )

    def update_strategy(
            self,
            reward: float,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None
    ) -> None:
        self.choose_card_strategy.update(reward, self.hand, board, current_round, current_turn)
        self.choose_row_strategy.update(reward, self.hand, board, current_round, current_turn)

    def choose_row(self, board: Optional[Board] = None) -> int:
        return self.choose_row_strategy.choose_row(hand=self.hand, board=board)

    def sort_hand(self):
        self.hand.sort()

    def reset_hand(self):
        self.hand.reset()

    def reset_points(self):
        self.total_points = 0
        self.round_points = []

    def add_points(self, points: int):
        self.total_points += points

    def copy(self) -> "BasePlayer":
        raise NotImplementedError(f"Implement copy method in {self.__class__.__name__}")
