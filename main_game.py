from src.controller.controller import GameController
from src.controller.controller_args import parse_controller_args
from src.model.game_config import GameConfig


def main():
    # TODO get config as input argument
    args = parse_controller_args()
    game_config = GameConfig.get_test_config(num_players=args.num_players)
    controller = GameController(game_config, seed=args.seed)
    controller.play()


if __name__ == '__main__':
    main()
