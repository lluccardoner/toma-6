from typing import Optional, Dict

from src.logger import LoggingMode, get_controller_logger_by_mode
from src.model.board import Board
from src.model.card import Card
from src.model.card_deck import CardDeck
from src.model.game_config import GameConfig
from src.model.player.base_player import BasePlayer
from src.model.player.player_factory import PlayerFactory
from src.view import View

CARDS_PER_PLAYER = 10
ROUNDS_PER_GAME = 4
MAX_ROW_LENGTH = 5
MAX_PLAYERS = 10


class GameController:
    def __init__(self, config: GameConfig, seed: Optional[int] = None,
                 logging_mode: Optional[LoggingMode] = LoggingMode.TO_CONSOLE_VERBOSE,
                 logger_file: Optional[str] = None):
        self.logger = get_controller_logger_by_mode(logging_mode, logger_file)
        self.seed = seed
        # Model
        self.deck = CardDeck(seed=self.seed)
        self.board = Board()
        self.players = [PlayerFactory.create_player(player_config, seed=self.seed) for player_config in config.players]
        self.players_dict = {player.name: player for player in self.players}
        self.num_players = len(self.players)
        assert self.num_players <= MAX_PLAYERS, f"Number of players should be maximum {MAX_PLAYERS}"
        # View
        self.view = View(self.board, self.players, logging_mode=logging_mode, logger_file=logger_file)
        # Init game
        self.deck.shuffle()

    def play(self) -> BasePlayer:
        self.logger.info(f"Starting game [seed={self.seed}]")
        for player in self.players:
            player.reset_points()

        for game_round in range(1, ROUNDS_PER_GAME + 1):
            self.logger.info(f"Starting round {game_round}")

            self.deck.reset_and_shuffle()
            self.board.reset()
            self.deal_cards()
            self.initialize_board()
            self.view.display_game()

            for turn in range(1, CARDS_PER_PLAYER + 1):
                self.logger.info(f"Playing round:{game_round}|turn:{turn}")

                chosen_cards = self.choose_cards()
                self.view.display_chosen_cards(chosen_cards)
                self.play_cards(chosen_cards)
                self.view.display_game()

            for player in self.players:
                previous_point_rounds = sum(player.round_points)
                player.round_points.append(player.total_points - previous_point_rounds)

        winner = min(self.players, key=lambda p: p.total_points)
        self.view.display_results()
        return winner

    def deal_cards(self):
        self.logger.info(f"Dealing {CARDS_PER_PLAYER} cards to each player...")
        for player in self.players:
            player.reset_hand()
            for _ in range(CARDS_PER_PLAYER):
                card = self.deck.cards.pop()
                player.hand.add_card(card)
            player.sort_hand()

    def initialize_board(self):
        self.logger.info("Initializing board...")
        for row in self.board.rows:
            card = self.deck.cards.pop()
            row.append(card)

    def choose_cards(self) -> Dict[str, Card]:
        self.logger.info("Players choose cards...")
        chosen_cards = [(player.name, player.choose_card(board=self.board)) for player in self.players]
        # Lowest card will play first
        chosen_cards.sort(key=lambda x: x[1].value)
        return dict(chosen_cards)

    def play_cards(self, chosen_cards: dict[str, Card]):
        self.logger.info("Playing cards...")
        for player_name, chosen_card in chosen_cards.items():
            player = self.players_dict[player_name]
            row_index = self.find_valid_row(chosen_card)

            play_str = f"{player_name} -> "
            if row_index is not None:
                play_str += f"Must play card in row {row_index + 1}"
                row = self.board.rows[row_index]
                if len(row) < MAX_ROW_LENGTH:
                    row.append(chosen_card)
                else:
                    self.nyam_nyam_nyam(row_index, chosen_card, player)

            else:
                chosen_row = player.choose_row(board=self.board)
                play_str += f"Can't play the card -> Chose row {chosen_row + 1}"
                self.nyam_nyam_nyam(chosen_row, chosen_card, player)

            self.logger.info(play_str)

    def find_valid_row(self, card: Card) -> Optional[int]:
        valid_rows = {
            idx: card.value - row[-1].value
            for idx, row in enumerate(self.board.rows)
            if card.value > row[-1].value
        }
        return min(valid_rows, key=valid_rows.get) if valid_rows else None

    def nyam_nyam_nyam(self, row_index: int, played_card: Card, player: BasePlayer):
        # Take row
        row = self.board.rows[row_index]
        player.total_points += sum(card.points for card in row)
        self.board.rows[row_index] = [played_card]
