from src.model.game_config import GameConfig
from src.simulation.simulation import Simulation
from src.simulation.simulation_args import parse_simulation_args


def main():
    args = parse_simulation_args()
    game_configs = [GameConfig.load(config) for config in args.configs]
    for game_config in game_configs:
        simulation = Simulation(game_config, num_games=args.num_games, seed=args.seed)
        simulation.run()


if __name__ == '__main__':
    main()
