from typing import Optional

from src.model.game_config import PlayerConfig, PlayerType
from src.model.player.base_player import BasePlayer
from src.model.player.input_player import InputPlayer
from src.model.player.level_player import MinPlayer, MidPlayer, MaxPlayer
from src.model.player.random_player import RandomPlayer
from src.model.player.rl_player import RLPlayerLearner


class PlayerFactory:
    @staticmethod
    def create_player(player_config: PlayerConfig, seed: Optional[int] = None) -> BasePlayer:
        player_dict = {
            PlayerType.RANDOM: RandomPlayer(player_config.name, seed=seed),
            PlayerType.MIN: MinPlayer(player_config.name),
            PlayerType.MID: MidPlayer(player_config.name),
            PlayerType.MAX: MaxPlayer(player_config.name),
            PlayerType.INPUT: InputPlayer(player_config.name),
            PlayerType.RL_LEARNER: RLPlayerLearner(player_config.name),
        }
        player_type = player_config.player_type
        if player_type not in player_dict:
            raise ValueError(f"Unsupported player type: {player_config.player_type}")
        return player_dict[player_type]
