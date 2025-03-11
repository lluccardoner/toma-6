from collections import OrderedDict
from typing import OrderedDict as OrderedDictType, Optional

from model.board import Board
from model.card import Card
from model.card_deck import CardDeck
from model.player.base_player import BasePlayer
from model.player.random_player import RandomPlayer
from view import View

CARDS_PER_PLAYER = 10
ROUNDS_PER_GAME = 4
MAX_ROW_LENGTH = 5

CARD_DECK = [Card(i) for i in range(1, 105)]


class GameController:
    def __init__(self, num_players: int, seed: Optional[int] = None):
        self.seed = seed
        # Model
        self.deck = CardDeck(seed)
        self.board = Board()
        self.players = [RandomPlayer(f"Player {i + 1}") for i in range(num_players)]
        self.players_dict = {player.name: player for player in self.players}
        # View
        self.view = View(self.board, self.players)
        # Init game
        self.deck.shuffle()

    def play(self) -> BasePlayer:
        for player in self.players:
            player.reset_points()

        for game_round in range(1, ROUNDS_PER_GAME + 1):
            print(f"Starting round {game_round}")
            self.deck.reset()
            self.board.reset()
            self.deal_cards()
            self.initialize_board()
            self.view.display_game()
            for turn in range(1, CARDS_PER_PLAYER + 1):
                print(f"Playing round:{game_round}|turn:{turn}")
                chosen_cards = self.choose_cards()
                self.view.display_chosen_cards(chosen_cards)
                self.play_cards(chosen_cards)
                self.view.display_game()
            for player in self.players:
                previous_point_rounds = sum(player.round_points)
                player.round_points.append(player.total_points - previous_point_rounds)

        # Winner
        result = {player.name: {"total": player.total_points, "rounds": player.round_points} for player in self.players}
        sorted_result = OrderedDict(sorted(result.items(), key=lambda item: item[1]["total"], reverse=False))

        print("Results:")
        print("\n".join(
            f"{player_name} -> total: {points["total"]}, rounds: {points["rounds"]}" for player_name, points in
            sorted_result.items()))

        winner_player_name, _ = sorted_result.popitem(last=False)
        return [player for player in self.players if player.name == winner_player_name][0]

    def deal_cards(self):
        print(f"Dealing {CARDS_PER_PLAYER} cards to each player...")
        for player in self.players:
            player.reset_hand()
            for _ in range(CARDS_PER_PLAYER):
                player.hand.append(self.deck.cards.pop())
            player.hand.sort(key=lambda card: card.value)

    def initialize_board(self):
        print("Initializing board...")
        for row in self.board.rows:
            card = self.deck.cards.pop()
            row.append(card)

    def choose_cards(self) -> OrderedDictType[str, Card]:
        print("Players choose cards...")
        chosen_cards = [(player.name, player.choose_card()) for player in self.players]
        # Lowest card will play first
        chosen_cards.sort(key=lambda x: x[1].value)
        chosen_cards = OrderedDict(chosen_cards)
        return chosen_cards

    def play_cards(self, chosen_cards: OrderedDictType[str, Card]):
        print("Playing cards...")
        for player_name, chosen_card in chosen_cards.items():
            player = [player for player in self.players if player.name == player_name][0]

            card_value = chosen_card.value
            row_last_card_values = [row[-1].value for row in self.board.rows]

            # Compute the differences between the card and the last row values
            diffs = {row_number: card_value - row_last_value for row_number, row_last_value in
                     enumerate(row_last_card_values)}
            ascending_diffs = {row_number: diff for row_number, diff in diffs.items() if diff > 0}

            play_str = f"{player_name} -> "
            if ascending_diffs:
                min_ascending_diff_row = min(ascending_diffs, key=ascending_diffs.get)
                row = self.board.rows[min_ascending_diff_row]
                row_length = len(row)
                play_str += f"Must play card in row {min_ascending_diff_row + 1}"
                if row_length >= MAX_ROW_LENGTH:
                    play_str += " -> Must take the row cards"
                    self.nyam_nyam_nyam(min_ascending_diff_row, chosen_card, player)
                else:
                    row.append(chosen_card)

            else:
                chosen_row = player.choose_row()
                play_str += f"Can't play the card -> Chose row {chosen_row + 1}"
                self.nyam_nyam_nyam(chosen_row, chosen_card, player)

            print(play_str)

    def nyam_nyam_nyam(self, row_number: int, played_card: Card, player: BasePlayer):
        # Take row
        row = self.board.rows[row_number]
        row_points = sum([card.points for card in row])
        player.total_points += row_points
        self.board.rows[row_number] = [played_card]
