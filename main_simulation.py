from src.controller.controller import GameController
from src.controller.controller_args import parse_controller_args
from src.model.game_config import GameConfig
from src.simulation import Simulation


def main():
    # TODO in simulations, do not print the output, store it in file?
    # TODO list of configs
    # TODO save results
    # TODO save plot
    game_config = GameConfig.get_test_config(num_players=3)
    simulation = Simulation(game_config, num_games=100, seed=42)
    simulation.run()


if __name__ == '__main__':
    main()
