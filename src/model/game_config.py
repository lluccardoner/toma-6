from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List, Optional, Dict


class PlayerType(StrEnum):
    RANDOM = auto()


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
        seed = config_dict.get("seed")
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
