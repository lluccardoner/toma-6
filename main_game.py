from src.controller.controller import GameController
from src.controller.controller_args import parse_controller_args
from src.model.game_config import GameConfig
from src.model.player.player_factory import PlayerFactory


def main():
    args = parse_controller_args()
    game_config = GameConfig.load(args.config)
    players = [
        PlayerFactory.create_player(player_config, seed=args.seed)
        for player_config
        in game_config.players
    ]
    controller = GameController(players, seed=args.seed)
    controller.play()


if __name__ == '__main__':
    main()
