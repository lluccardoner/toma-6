import argparse

from src.simulation.simulation_args import SIMULATION_ARGS

EVOLUTION_STRATEGY_ARGS = SIMULATION_ARGS + [
    {
        'flags': ['--population'],
        'kwargs': {
            'type': int,
            'default': 50,
            'help': 'Population size for the evolution strategy.'
        }
    },
    {
        'flags': ['--sigma'],
        'kwargs': {
            'type': float,
            'default': 0.1,
            'help': 'Standard deviation of the noise added to the parameters.'
        }
    },
    {
        'flags': ['--lr'],
        'kwargs': {
            'type': float,
            'default': 0.03,
            'help': 'Learning rate for the evolution strategy.'
        }
    },
    {
        'flags': ['--lr-decay'],
        'kwargs': {
            'type': float,
            'default': 0.992354,
            'help': 'Learning rate decay factor per generation.'
        }
    },
]


def parse_evolution_strategy_args():
    parser = argparse.ArgumentParser(description="Run a Toma 6 game simulation with evolution strategy.")
    for arg in EVOLUTION_STRATEGY_ARGS:
        parser.add_argument(*arg['flags'], **arg['kwargs'])
    return parser.parse_args()
