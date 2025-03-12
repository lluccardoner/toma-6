import argparse


def parse_controller_args():
    parser = argparse.ArgumentParser(description="Run a Toma 6 game simulation.")

    parser.add_argument(
        "--num-players",
        type=int,
        required=True,
        help="Number of players in the game (e.g., 2-10)"
    )

    parser.add_argument(
        "--seed",
        type=int,
        required=False,
        default=None,
        help="Random seed for reproducibility (optional)"
    )

    return parser.parse_args()
