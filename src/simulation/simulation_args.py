import argparse


def parse_simulation_args():
    parser = argparse.ArgumentParser(description="Run a Toma 6 game simulation.")

    parser.add_argument(
        "--configs",
        required=False,
        nargs='+',
        default=["1-random_2.json"],
        help="Game configs for the simulation. Defaults to ['1-random_2.json']."
    )

    parser.add_argument(
        "--num-games",
        type=int,
        required=False,
        default=500,
        help="Number of games to run. Default 500."
    )

    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=None,
        help="Random seed for reproducibility (optional)."
    )

    return parser.parse_args()
