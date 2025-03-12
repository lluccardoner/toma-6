from typing import List

from src.model.board import Board
from src.model.card import Card
from src.model.player.base_player import BasePlayer


class View:
    def __init__(self, board, players):
        self.board: Board = board
        self.players: List[BasePlayer] = players

    def display_game(self):
        print("\n")
        print("#" * 10)
        self.display_board()
        print("-" * 10)
        self.display_players()
        print("#" * 10)
        print("\n")

    def display_board(self):
        for i, row in enumerate(self.board.rows):
            print(f"Row {i + 1}: {[card.value for card in row]}")

    def display_players(self):
        for player in self.players:
            print(f"{player.name}: {player.total_points} points {[card.value for card in player.hand]}")

    @staticmethod
    def display_chosen_cards(chosen_cards: dict[str, Card]):
        print("\n".join([f"{player_name} -> {card.value}" for player_name, card in chosen_cards.items()]))

    def display_results(self):
        for player in sorted(self.players, key=lambda p: p.total_points):
            print(f"{player.name} -> total: {player.total_points}, rounds: {player.round_points}")
