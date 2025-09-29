import unittest

from src.model.card import Card
from src.model.hand import Hand
from src.model.board import Board
from src.model.rl.state import State


class TestState(unittest.TestCase):

    def test_get_sorted_top_card_buckets(self):
        board = Board()
        board.rows[0].append(Card(10)) # Bucket 1: 10-19
        board.rows[1].append(Card(5)) # Bucket 0: 0-9
        board.rows[2].append(Card(12)) # Bucket 1: 10-19
        board.rows[3].append(Card(55)) # Bucket 5: 50-59

        buckets = State.get_top_card_buckets(board)

        self.assertTupleEqual(buckets, (1, 0, 1, 5))

    def test_get_row_lengths(self):
        board = Board()
        board.rows[0].append(Card(2))
        board.rows[0].append(Card(3))
        board.rows[1].append(Card(4))
        # row 2 stays empty
        board.rows[3].append(Card(5))
        board.rows[3].append(Card(6))
        board.rows[3].append(Card(7))

        lengths = State.get_row_lengths(board)

        self.assertTupleEqual(lengths, (2, 1, 0, 3))

    def test_get_row_points(self):
        board = Board()
        # Row 0: points 2 -> bucket 0
        board.rows[0].append(Card(5))
        # Row 1: points 5 -> bucket 1
        board.rows[1].append(Card(11))
        # Row 2: 0 points -> bucket 0
        # Row 3: points 1 + 7 = 12 -> bucket 2
        board.rows[3].append(Card(1))
        board.rows[3].append(Card(55))

        point_buckets = State.get_row_points_buckets(board)

        self.assertTupleEqual(point_buckets, (0, 1, 0, 2))

    def test_get_hand_histogram(self):
        hand = Hand()
        hand.add_card(Card(3))  # Bucket 0: 0-9
        hand.add_card(Card(7))  # Bucket 0: 0-9
        # Bucket 1: 10-19 is empty
        hand.add_card(Card(22)) # Bucket 2: 20-29
        hand.add_card(Card(35)) # Bucket 3: 30-39
        hand.add_card(Card(47)) # Bucket 4: 40-49
        hand.add_card(Card(58)) # Bucket 5: 50-59
        hand.add_card(Card(69)) # Bucket 6: 60-69
        # Bucket 7: 70-79 is empty
        hand.add_card(Card(80)) # Bucket 8: 80-89
        hand.add_card(Card(99)) # Bucket 9: 90-99
        hand.add_card(Card(104)) # Bucket 10: 100+

        histogram = State.get_hand_histogram(hand)

        expected_histogram = (2, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1)
        self.assertTupleEqual(histogram, expected_histogram)

    def test_create(self):
        board = Board()
        board.rows[0].append(Card(20))
        board.rows[1].append(Card(15))
        board.rows[2].append(Card(11))
        board.rows[3].append(Card(1))

        state_tuple = State.create(board)

        expected = (
            2,1,1,0, # top_card_buckets
        )

        self.assertTupleEqual(state_tuple, expected)

    def test_get_all_states_length(self):
        all_states = State.get_all_states()
        self.assertEqual(len(all_states), 14641)


if __name__ == '__main__':
    unittest.main()

