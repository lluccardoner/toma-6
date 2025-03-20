import unittest

from parameterized import parameterized

from src.model.board import Board
from src.model.card import Card


class TestBoard(unittest.TestCase):

    def test_reset(self):
        # Arrange
        board = Board()
        card = Card(5)
        board.rows[0].append(card)

        # Act
        board.reset()

        # Assert
        self.assertTrue(all(len(row) == 0 for row in board.rows))

    def test_get_points_per_row(self):
        # Arrange
        board = Board()
        card1 = Card(5)
        card2 = Card(10)
        board.rows[0].append(card1)
        board.rows[1].append(card2)

        # Act
        points = board.get_points_per_row()

        # Assert
        self.assertEqual(points, [2, 3, 0, 0])

    @parameterized.expand([
        (Card(7), 3),
        (Card(4), 1),
        (Card(1), None),
    ])
    def test_find_valid_row(self, new_card, expected):
        # Arrange
        board = Board()
        board.rows[0].append(Card(2))
        board.rows[1].append(Card(3))
        board.rows[2].append(Card(5))
        board.rows[3].append(Card(6))

        # Act
        valid_row = board.find_valid_row(new_card)

        # Assert
        self.assertEqual(valid_row, expected)


if __name__ == '__main__':
    unittest.main()
