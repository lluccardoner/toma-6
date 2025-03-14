import argparse


def parse_controller_args():
    parser = argparse.ArgumentParser(description="Run a Toma 6 game.")

    parser.add_argument(
        "--config",
        type=str,
        required=False,
        default="1_random_2.json",
        help="Config for the game. Defaults to '1_random_2.json'"
    )

    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=None,
        help="Random seed for reproducibility (optional)"
    )

    return parser.parse_args()
