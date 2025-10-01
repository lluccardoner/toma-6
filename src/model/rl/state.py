from itertools import product
from typing import Tuple, List

from src.model.board import Board
from src.model.hand import Hand
from itertools import combinations_with_replacement


class State:

    @classmethod
    def get_all_states(cls) -> List[Tuple]:
        # states = []
        #
        # top_card_range = range(11)
        #
        # for top_cards in product(top_card_range, repeat=4):  # 4 rows
        #     state = top_cards
        #     states.append(state)

        states = list(combinations_with_replacement(range(11), 4))  # 1001 tuples

        return states

    @classmethod
    def create(cls, board: Board):
        # For now, we only use the top card buckets to represent the state of the game
        top_card_buckets = cls.get_top_card_buckets(board)
        return top_card_buckets

    @classmethod
    def get_top_card_buckets(cls, board: Board) -> Tuple[int, int, int, int]:
        last_row_cards = board.get_last_row_cards()
        # 11 buckets for card values: 0-9, 10-19, ..., 90-99, 100+
        last_row_cards_buckets = [card.value // 10 for card in last_row_cards]
        return tuple(sorted(last_row_cards_buckets))

    @classmethod
    def get_row_lengths(cls, board: Board) -> Tuple[int, int, int, int]:
        # 4 rows, each with lengths 1-5
        return tuple(len(row) for row in board.rows)

    @classmethod
    def get_row_points_buckets(cls, board: Board) -> Tuple[int, int, int, int]:
        # 4 rows, each with bucketed by points 0: 0-2, 1: 3-5, 2: >=6
        row_points = board.get_points_per_row()
        row_points_buckets = tuple(
            0 if points <= 2 else 1 if points <= 5 else 2
            for points in row_points
        )
        return row_points_buckets

    @classmethod
    def get_hand_histogram(cls, hand: Hand) -> Tuple[int, int, int, int, int, int, int, int, int, int]:
        # Histogram of hand card values -> 11 buckets: 0-9, 10-19, ..., 90-99, 100+
        histogram = [0] * 11
        for card in hand:
            index = card.value // 10
            histogram[index] += 1
        return tuple(histogram)
