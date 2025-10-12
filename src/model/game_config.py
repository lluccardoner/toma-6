import json
import os
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List, Dict, Optional

from src.logger import get_default_logger

CONFIG_PATH = "config"

config_logger = get_default_logger("GameConfig")


class PlayerType(StrEnum):
    RANDOM = auto()
    MIN = auto()
    MID = auto()
    MAX = auto()
    INPUT = auto()
    RL_LEARNER = auto()
    RL_PLAYER = auto()  # Use Q-learning strategy for training
    RL_ES_LEARNER = auto()
    RL_ES_PLAYER = auto()  # Use Evolution Strategy for training


@dataclass
class RLConfig:
    q_path: Optional[str] = None
    policy_nn_params_path: Optional[str] = None

    @staticmethod
    def from_dict(config_dict: Dict) -> "RLConfig":
        return RLConfig(
            q_path=config_dict.get("q_path"),
            policy_nn_params_path=config_dict.get("policy_nn_params_path"),
        )


@dataclass
class PlayerConfig:
    name: str
    player_type: PlayerType
    rl_config: Optional[RLConfig] = None

    @staticmethod
    def from_dict(config_dict: Dict) -> "PlayerConfig":
        rl_config = None
        if rl_config_dict := config_dict.get("rl_config"):
            rl_config = RLConfig.from_dict(rl_config_dict)
        return PlayerConfig(
            name=config_dict["name"],
            player_type=PlayerType(config_dict["type"]),
            rl_config=rl_config
        )


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
                PlayerConfig.from_dict(player)
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
