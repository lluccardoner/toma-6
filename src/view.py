from typing import List, Optional

from src.logger import get_view_logger
from src.model.board import Board
from src.model.card import Card
from src.model.player.base_player import BasePlayer


class View:
    def __init__(self, board: Board, players: List[BasePlayer], logger_file: Optional[str] = None):
        self.logger = get_view_logger(logger_file)
        self.board: Board = board
        self.players: List[BasePlayer] = players

    def display_game(self):
        self.logger.info("\n")
        self.logger.info("#" * 10)
        self.display_board()
        self.logger.info("-" * 10)
        self.display_players()
        self.logger.info("#" * 10)
        self.logger.info("\n")

    def display_board(self):
        for i, row in enumerate(self.board.rows):
            self.logger.info(f"Row {i + 1}: {[card.value for card in row]}")

    def display_players(self):
        for player in self.players:
            self.logger.info(f"{player.name}: {player.total_points} points {[card.value for card in player.hand]}")

    def display_chosen_cards(self, chosen_cards: dict[str, Card]):
        self.logger.info("\n".join([f"{player_name} -> {card.value}" for player_name, card in chosen_cards.items()]))

    def display_results(self):
        self.logger.info("Results:")
        for player in sorted(self.players, key=lambda p: p.total_points):
            self.logger.info(f"{player.name} -> total: {player.total_points}, rounds: {player.round_points}")
