from typing import Optional

from src.model.game_config import PlayerConfig, PlayerType
from src.model.player.base_player import BasePlayer
from src.model.player.random_player import RandomPlayer


class PlayerFactory:
    @staticmethod
    def create_player(player_config: PlayerConfig, seed: Optional[int] = None) -> BasePlayer:
        if player_config.player_type == PlayerType.RANDOM:
            return RandomPlayer(player_config.name, seed=seed)
        else:
            raise ValueError(f"Unsupported player type: {player_config.player_type}")
