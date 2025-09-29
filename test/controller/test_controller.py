import unittest
from unittest.mock import MagicMock

from src.model.player.player_factory import PlayerFactory
from src.controller.controller import GameController
from src.logger import LoggingMode
from src.model.card import Card
from src.model.game_config import GameConfig, PlayerConfig, PlayerType
from src.model.player.base_player import BasePlayer


class TestGameController(unittest.TestCase):

    def setUp(self):
        self.config = GameConfig(
            game_id='test-game',
            name='Test Game',
            players=[
                PlayerConfig(name='TestPlayer1', player_type=PlayerType.RANDOM),
                PlayerConfig(name='TestPlayer2', player_type=PlayerType.RANDOM)
            ]
        )
        self.players = [PlayerFactory.create_player(player_config) for player_config in self.config.players]

    def test_deal_cards(self):
        # Arrange
        controller = GameController(players=self.players, seed=42, logging_mode=LoggingMode.TO_CONSOLE_VERBOSE)

        # Act
        controller.deal_cards()

        # Assert
        for player in controller.players:
            self.assertEqual(len(player.hand.cards), 10)

    def test_initialize_board(self):
        # Arrange
        controller = GameController(players=self.players, seed=42, logging_mode=LoggingMode.TO_CONSOLE_VERBOSE)

        # Act
        controller.initialize_board()

        # Assert
        for row in controller.board.rows:
            self.assertEqual(len(row), 1)

    def test_choose_cards(self):
        # Arrange
        controller = GameController(players=self.players, seed=42, logging_mode=LoggingMode.TO_CONSOLE_VERBOSE)
        controller.players[0].choose_card = MagicMock(return_value=Card(10))
        controller.players[1].choose_card = MagicMock(return_value=Card(5))
        expected_chosen_cards = {"TestPlayer2": Card(5), "TestPlayer1": Card(10)}

        # Act
        chosen_cards = controller.choose_cards(game_round=1, round_turn=1)

        # Assert
        self.assertEqual(len(chosen_cards), 2)
        # Chosen cards are sorted
        self.assertDictEqual(chosen_cards, expected_chosen_cards)
        self.assertDictEqual(controller.game_history.get_history()[1][1]['chosen_cards'], expected_chosen_cards)

    def test_play_cards(self):
        # Arrange
        controller = GameController(players=self.players, seed=42, logging_mode=LoggingMode.TO_CONSOLE_VERBOSE)
        player_1 = MagicMock(name="MockTestPlayer1", spec=BasePlayer)
        player_2 = MagicMock(name="MockTestPlayer2", spec=BasePlayer)
        controller.players_dict = {'TestPlayer1': player_1, 'TestPlayer2': player_2}
        controller.board.find_valid_row = MagicMock(return_value=0)  # All players will play in row 0
        controller.board.rows[0] = [Card(1), Card(2), Card(3), Card(4), Card(5)]
        chosen_cards = {'TestPlayer1': Card(6), 'TestPlayer2': Card(7)}

        # Act
        controller.play_cards(game_round=1, round_turn=1, chosen_cards=chosen_cards)

        # Assert
        self.assertEqual(len(controller.board.rows[0]), 2)  # Row got to 6 cards so it restarted
        self.assertEqual(controller.board.rows[0], [Card(6), Card(7)])  # Board status after playing cards

        player_1.choose_row.assert_not_called()
        player_1.add_points.assert_called_with(6)  # Player 1 got all row points
        player_1.update_strategy.assert_called_once()

        player_2.choose_row.assert_not_called()
        player_2.add_points.assert_not_called()
        player_2.update_strategy.assert_called_once()

        self.assertDictEqual(
            controller.game_history.get_history()[1][1]['chosen_rows'],
            {'TestPlayer1': (0, True), 'TestPlayer2': (None, False)}
        )

    def test_nyam_nyam_nyam(self):
        # Arrange
        controller = GameController(players=self.players, seed=42, logging_mode=LoggingMode.TO_CONSOLE_VERBOSE)
        player = controller.players[0]
        controller.board.rows[0] = [Card(1), Card(2), Card(3), Card(4), Card(5)]
        played_card = Card(6)

        # Act
        controller.nyam_nyam_nyam(0, played_card, player)

        # Assert
        self.assertEqual(player.total_points, 6)
        self.assertEqual(controller.board.rows[0], [played_card])


if __name__ == '__main__':
    unittest.main()
