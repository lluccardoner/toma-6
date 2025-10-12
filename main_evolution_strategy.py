from src.simulation.evolution_strategy_args import parse_evolution_strategy_args
from src.model.game_config import GameConfig
from src.simulation.evolution_strategy import EvolutionStrategy


def main():
    args = parse_evolution_strategy_args()
    game_configs = [GameConfig.load(config) for config in args.configs]
    for game_config in game_configs:
        evolution = EvolutionStrategy(
            game_config,
            num_games=args.num_games,
            seed=args.seed,
            population_size=args.population,
            sigma=args.sigma,
            lr=args.lr,
            lr_decay=args.lr_decay,
        )
        evolution.run()


if __name__ == '__main__':
    main()
