from typing import Optional

from src.model.game_config import PlayerConfig, PlayerType
from src.model.player.base_player import BasePlayer
from src.model.player.input_player import InputPlayer
from src.model.player.level_player import MinPlayer, MidPlayer, MaxPlayer
from src.model.player.random_player import RandomPlayer
from src.model.player.rl_q_value.rl_player import RLPlayerLearner, RLPlayer
from src.model.player.rl_q_value.rl_utils import load_Q_from_file


class PlayerFactory:
    @staticmethod
    def create_player(player_config: PlayerConfig, seed: Optional[int] = None) -> BasePlayer:
        # Use callables so player instances are created lazily when requested
        player_factories = {
            PlayerType.RANDOM: lambda: RandomPlayer(player_config.name, seed=seed),
            PlayerType.MIN: lambda: MinPlayer(player_config.name),
            PlayerType.MID: lambda: MidPlayer(player_config.name),
            PlayerType.MAX: lambda: MaxPlayer(player_config.name),
            PlayerType.INPUT: lambda: InputPlayer(player_config.name),
            PlayerType.RL_LEARNER: lambda: RLPlayerLearner(player_config.name),
            PlayerType.RL_PLAYER: lambda: PlayerFactory.load_rl_player(player_config),
        }
        player_type = player_config.player_type
        if player_type not in player_factories:
            raise ValueError(f"Unsupported player type: {player_type}")
        # Call the factory to create the player instance on demand
        return player_factories[player_type]()

    @staticmethod
    def load_rl_player(player_config: PlayerConfig) -> RLPlayer:
        q_file_path = player_config.rl_config.q_path
        Q = load_Q_from_file(q_file_path)
        return RLPlayer(player_config.name, Q=Q)
