import unittest

from src.model.card import Card
from src.model.hand import Hand
from src.model.strategy.choose_card.random_choose_card_strategy import RandomChooseCardStrategy


class TestRandomChooseCardStrategy(unittest.TestCase):

    def setUp(self):
        self.hand = Hand()
        self.hand.cards = [Card(5), Card(10), Card(15)]

    def test_choose_card(self):
        strategy = RandomChooseCardStrategy(seed=42)

        chosen_card = strategy.choose_card(hand=self.hand)

        self.assertEqual(chosen_card, Card(15))
        self.assertEqual(len(self.hand.cards), 2)

    def test_choose_card_randomness(self):
        strategy = RandomChooseCardStrategy(seed=43)

        chosen_card = strategy.choose_card(hand=self.hand)

        self.assertEqual(chosen_card, Card(5))
        self.assertEqual(len(self.hand.cards), 2)


if __name__ == '__main__':
    unittest.main()
