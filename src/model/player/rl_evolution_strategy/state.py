from typing import Tuple, List

import numpy as np

from src.model.board import Board
from src.model.hand import Hand

StateType = np.ndarray


class State:
    number_states: int = 23
    dimensions: Tuple[int, ...] = (number_states,)

    @classmethod
    def create(cls, board: Board, hand: Hand) -> StateType:
        board_top_cards = cls.get_top_cards(board)  # 4 values
        board_row_lengths = cls.get_row_lengths(board)  # 4 values
        board_row_points = cls.get_row_points(board)  # 4 values
        hand_histogram = cls.get_hand_histogram(hand)  # 11 values
        # Total: 4 + 4 + 4 + 11 = 23 values
        state = np.array(board_top_cards + board_row_lengths + board_row_points + hand_histogram)
        assert state.shape == cls.dimensions, f"State shape {state.shape} does not match expected {cls.dimensions}"
        return state

    @classmethod
    def get_top_cards(cls, board: Board) -> List[int]:
        last_row_cards = board.get_last_row_cards()
        return [card.value for card in last_row_cards]

    @classmethod
    def get_row_lengths(cls, board: Board) -> List[int]:
        return [len(row) for row in board.rows]

    @classmethod
    def get_row_points(cls, board: Board) -> List[int]:
        row_points = board.get_points_per_row()
        return row_points

    @classmethod
    def get_hand_histogram(cls, hand: Hand) -> List[int]:
        # Histogram of hand card values -> 11 buckets: 0-9, 10-19, ..., 90-99, 100+
        histogram = [0] * 11
        for card in hand:
            index = card.value // 10
            histogram[index] += 1
        return histogram
