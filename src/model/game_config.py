import json
import os
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List, Dict

from src.logger import get_default_logger

CONFIG_PATH = "config"

config_logger = get_default_logger("GameConfig")


class PlayerType(StrEnum):
    RANDOM = auto()
    MIN = auto()
    MID = auto()
    MAX = auto()
    INPUT = auto()
    RL = auto()


@dataclass
class PlayerConfig:
    name: str
    player_type: PlayerType


@dataclass
class GameConfig:
    game_id: str
    name: str
    players: List[PlayerConfig]

    @staticmethod
    def from_dict(config_dict: Dict) -> "GameConfig":
        return GameConfig(
            game_id=config_dict["game_id"],
            name=config_dict["name"],
            players=[
                PlayerConfig(
                    name=player["name"],
                    player_type=PlayerType(player["type"]),
                )
                for player in config_dict["players"]
            ],
        )

    @staticmethod
    def load(config_file_name: str) -> "GameConfig":
        config_file_path = os.path.join(CONFIG_PATH, config_file_name)
        with open(config_file_path, "r") as f:
            config_data = json.load(f)
            game_config = GameConfig.from_dict(config_data)
            config_logger.info(f"Loaded config id={game_config.game_id} from {config_file_path}")
            return game_config

    @staticmethod
    def get_test_config(num_players: int) -> "GameConfig":
        return GameConfig(
            game_id="0",
            name="Test game",
            players=[
                PlayerConfig(
                    name=f"Random player {i + 1}",
                    player_type=PlayerType.RANDOM,
                ) for i in range(num_players)
            ]
        )
