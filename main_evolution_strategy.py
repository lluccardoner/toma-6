from src.model.game_config import GameConfig
from src.simulation.evolution_strategy import EvolutionStrategy
from src.simulation.simulation_args import parse_simulation_args


def main():
    # TODO evolution strategy args
    args = parse_simulation_args()
    game_configs = [GameConfig.load(config) for config in args.configs]
    for game_config in game_configs:
        evolution = EvolutionStrategy(game_config, num_games=args.num_games, seed=args.seed)
        evolution.run(population_size=100, sigma=0.1, lr=0.03)


if __name__ == '__main__':
    main()
