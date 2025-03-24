from typing import Dict, Tuple

from src.model.card import Card


class GameHistory:
    def __init__(self, rounds: int, turns: int):
        self._history = {
            round_num: {
                turn_num: {
                    'chosen_cards': {},
                    'board_cards': [],
                    'chosen_rows': {}
                }
                for turn_num in range(1, turns + 1)
            }
            for round_num in range(1, rounds + 1)
        }

    def add_chosen_cards(self, round_num: int, turn_num: int, chosen_cards: Dict[str, Card]):
        # For each player name, the card chosen
        self._history[round_num][turn_num]['chosen_cards'] = chosen_cards

    def add_board_cards(self, round_num: int, turn_num: int, board_cards: list[list[Card]]):
        # For each row on the board, the list of cards
        self._history[round_num][turn_num]['board_cards'] = board_cards

    def add_chosen_rows(self, round_num: int, turn_num: int, chosen_rows: Dict[str, Tuple[int, bool]]):
        # For each player name, the chosen row index and whether the row was full or not
        self._history[round_num][turn_num]['chosen_rows'] = chosen_rows

    def get_history(self):
        return self._history
