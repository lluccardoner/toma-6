import unittest

from src.model.card import Card
from src.model.hand import Hand
from src.model.strategy.choose_card.level_choose_card_strategy import (
    LevelChooseCardStrategy,
    MinChooseCardStrategy,
    MidChooseCardStrategy,
    MaxChooseCardStrategy
)


class TestLevelChooseCardStrategy(unittest.TestCase):

    def setUp(self):
        self.hand = Hand()
        self.hand.cards = [Card(5), Card(10), Card(15)]

    def test_level_choose_card_strategy_lowest(self):
        strategy = LevelChooseCardStrategy(level=0)
        chosen_card = strategy.choose_card(hand=self.hand)
        self.assertEqual(chosen_card.value, 5)
        self.assertEqual(len(self.hand.cards), 2)

    def test_level_choose_card_strategy_highest(self):
        strategy = LevelChooseCardStrategy(level=1)
        chosen_card = strategy.choose_card(hand=self.hand)
        self.assertEqual(chosen_card.value, 15)
        self.assertEqual(len(self.hand.cards), 2)

    def test_level_choose_card_strategy_middle(self):
        strategy = LevelChooseCardStrategy(level=0.5)
        chosen_card = strategy.choose_card(hand=self.hand)
        self.assertEqual(chosen_card.value, 10)
        self.assertEqual(len(self.hand.cards), 2)

    def test_min_choose_card_strategy(self):
        strategy = MinChooseCardStrategy()
        chosen_card = strategy.choose_card(hand=self.hand)
        self.assertEqual(chosen_card.value, 5)
        self.assertEqual(len(self.hand.cards), 2)

    def test_mid_choose_card_strategy(self):
        strategy = MidChooseCardStrategy()
        chosen_card = strategy.choose_card(hand=self.hand)
        self.assertEqual(chosen_card.value, 10)
        self.assertEqual(len(self.hand.cards), 2)

    def test_max_choose_card_strategy(self):
        strategy = MaxChooseCardStrategy()
        chosen_card = strategy.choose_card(hand=self.hand)
        self.assertEqual(chosen_card.value, 15)
        self.assertEqual(len(self.hand.cards), 2)


if __name__ == '__main__':
    unittest.main()
