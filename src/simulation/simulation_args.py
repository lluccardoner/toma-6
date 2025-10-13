import argparse

SIMULATION_ARGS = [
    {
        'flags': ['--configs'],
        'kwargs': {
            'required': False,
            'nargs': '+',
            'default': ["1-random_2.json"],
            'help': "Game configs for the simulation. Defaults to ['1-random_2.json']."
        }
    },
    {
        'flags': ['--num-games'],
        'kwargs': {
            'type': int,
            'required': False,
            'default': 500,
            'help': 'Number of games to run. Default 500.'
        }
    },
    {
        'flags': ['--seed'],
        'kwargs': {
            'type': int,
            'required': False,
            'default': None,
            'help': 'Random seed for reproducibility (optional).'
        }
    },
    {
        'flags': ['--equal-games'],
        'kwargs': {
            'action': 'store_true',
            'help': 'If set, all games will have the same seed, making them identical.'
        }
    }
]


def parse_simulation_args():
    parser = argparse.ArgumentParser(description="Run a Toma 6 game simulation.")
    for arg in SIMULATION_ARGS:
        parser.add_argument(*arg['flags'], **arg['kwargs'])
    return parser.parse_args()
