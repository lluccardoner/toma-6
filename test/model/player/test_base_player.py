import unittest
from unittest.mock import MagicMock

from src.model.card import Card
from src.model.hand import Hand
from src.model.player.base_player import BasePlayer
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy
from src.model.strategy.choose_row.base_choose_row_strategy import BaseChooseRowStrategy


class TestBasePlayer(unittest.TestCase):

    def setUp(self):
        self.choose_card_strategy = MagicMock(spec=BaseChooseCardStrategy)
        self.choose_row_strategy = MagicMock(spec=BaseChooseRowStrategy)
        self.player = BasePlayer(
            name="TestPlayer",
            choose_card_strategy=self.choose_card_strategy,
            choose_row_strategy=self.choose_row_strategy
        )

    def test_initialization(self):
        # Arrange & Act
        player = self.player

        # Assert
        self.assertEqual(player.name, "TestPlayer")
        self.assertIsInstance(player.hand, Hand)
        self.assertEqual(player.total_points, 0)
        self.assertEqual(player.round_points, [])

    def test_choose_card(self):
        # Arrange
        card = Card(5)
        self.choose_card_strategy.choose_card.return_value = card

        # Act
        chosen_card = self.player.choose_card()

        # Assert
        self.assertEqual(chosen_card, card)
        self.choose_card_strategy.choose_card.assert_called_once_with(
            hand=self.player.hand,
            board=None,
            current_round=None,
            current_turn=None,
            game_history=None
        )

    def test_choose_row(self):
        # Arrange
        row_index = 1
        self.choose_row_strategy.choose_row.return_value = row_index

        # Act
        chosen_row = self.player.choose_row()

        # Assert
        self.assertEqual(chosen_row, row_index)
        self.choose_row_strategy.choose_row.assert_called_once_with(hand=self.player.hand, board=None)

    def test_sort_hand(self):
        # Arrange
        self.player.hand.sort = MagicMock()

        # Act
        self.player.sort_hand()

        # Assert
        self.player.hand.sort.assert_called_once()

    def test_reset_hand(self):
        # Arrange
        self.player.hand.reset = MagicMock()

        # Act
        self.player.reset_hand()

        # Assert
        self.player.hand.reset.assert_called_once()

    def test_reset_points(self):
        # Arrange
        self.player.total_points = 10
        self.player.round_points = [1, 2, 3]

        # Act
        self.player.reset_points()

        # Assert
        self.assertEqual(self.player.total_points, 0)
        self.assertEqual(self.player.round_points, [])


if __name__ == '__main__':
    unittest.main()
