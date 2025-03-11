import random

import matplotlib.pyplot as plt

from controler import GameController


class Simulation:
    def __init__(self, num_players: int, num_games: int = 100):
        self.num_players = num_players
        self.num_games = num_games
        self.results = [0] * num_players

    def run(self):
        for _ in range(self.num_games):
            game = GameController(self.num_players)
            game.deal_cards()
            # Simplified game logic placeholder
            winner = random.randint(0, self.num_players - 1)
            self.results[winner] += 1

    def plot_results(self):
        plt.bar([f"Player {i + 1}" for i in range(self.num_players)], self.results)
        plt.title("Wins per Player")
        plt.show()
