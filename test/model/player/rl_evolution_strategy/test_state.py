import unittest

import numpy as np

from src.model.board import Board
from src.model.card import Card
from src.model.hand import Hand
from src.model.player.rl_evolution_strategy.state import State


class TestState(unittest.TestCase):

    def test_should_return_top_cards_values(self):
        board = Board()
        board.rows[0].append(Card(10))
        board.rows[1].append(Card(55))
        board.rows[2].append(Card(25))
        board.rows[3].append(Card(99))

        top_cards = State.get_top_cards(board)

        expected = np.array([10, 55, 25, 99])
        np.testing.assert_array_equal(top_cards, expected)

    def test_should_return_row_lengths_when_board_has_mixed_rows(self):
        board = Board()
        board.rows[0].append(Card(2))
        board.rows[0].append(Card(3))
        board.rows[1].append(Card(4))
        # row 2 stays empty
        board.rows[3].append(Card(5))
        board.rows[3].append(Card(6))
        board.rows[3].append(Card(7))

        lengths = State.get_row_lengths(board)

        expected = np.array([2, 1, 0, 3])
        np.testing.assert_array_equal(lengths, expected)

    def test_should_return_row_points_when_board_has_cards_with_points(self):
        board = Board()
        # Row 0: points 2
        board.rows[0].append(Card(5))
        # Row 1: points 5
        board.rows[1].append(Card(11))
        # Row 2: 0 points (empty)
        # Row 3: points 1 + 7 = 8
        board.rows[3].append(Card(1))
        board.rows[3].append(Card(55))

        row_points = State.get_row_points(board)

        expected = np.array([2, 5, 0, 8])
        np.testing.assert_array_equal(row_points, expected)

    def test_should_return_hand_histogram_when_hand_has_cards_in_different_buckets(self):
        hand = Hand()
        hand.cards = [
            Card(3),  # Bucket 0: 0-9
            Card(7),  # Bucket 0: 0-9
            Card(22),  # Bucket 2: 20-29
            Card(35),  # Bucket 3: 30-39
            Card(47),  # Bucket 4: 40-49
            Card(58),  # Bucket 5: 50-59
            Card(69),  # Bucket 6: 60-69
            Card(80),  # Bucket 8: 80-89
            Card(99),  # Bucket 9: 90-99
            Card(104),  # Bucket 10: 100+
        ]

        histogram = State.get_hand_histogram(hand)

        expected = np.array([2, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1])
        np.testing.assert_array_equal(histogram, expected)

    def test_should_create_state_with_correct_dimensions_when_board_and_hand_provided(self):
        board = Board()
        board.rows[0].append(Card(20))
        board.rows[1].append(Card(15))
        board.rows[2].append(Card(11))
        board.rows[3].append(Card(1))

        hand = Hand()
        hand.cards = [Card(25), Card(35), Card(45)]

        state = State.create(board, hand)

        self.assertEqual(state.shape, (23,))
        self.assertIsInstance(state, np.ndarray)

    def test_should_have_correct_class_attributes(self):
        self.assertEqual(State.number_states, 23)
        self.assertEqual(State.dimensions, (23,))


if __name__ == '__main__':
    unittest.main()
