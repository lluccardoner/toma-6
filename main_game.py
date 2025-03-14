from src.controller.controller import GameController
from src.controller.controller_args import parse_controller_args
from src.model.game_config import GameConfig


def main():
    args = parse_controller_args()
    game_config = GameConfig.load(args.config)
    controller = GameController(game_config, seed=args.seed)
    controller.play()


if __name__ == '__main__':
    main()
