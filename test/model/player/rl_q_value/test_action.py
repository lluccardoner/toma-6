# Updated to use unittest style consistent with other tests
import unittest

from src.model.player.rl_q_value.action import Action
from src.model.hand import Hand
from src.model.card import Card


class TestAction(unittest.TestCase):

    def test_lower_returns_min_card(self):
        hand = Hand()
        hand.add_card(Card(7))
        hand.add_card(Card(3))
        hand.add_card(Card(5))

        card = Action.to_card(Action.LOWER, hand)

        self.assertEqual(card, Card(3))

    def test_medium_returns_mid_card_with_odd_count(self):
        hand = Hand()
        hand.add_card(Card(10))
        hand.add_card(Card(1))
        hand.add_card(Card(6))

        card = Action.to_card(Action.MEDIUM, hand)

        self.assertEqual(card, Card(6))

    def test_medium_returns_mid_card_with_even_count(self):
        hand = Hand()
        hand.add_card(Card(8))
        hand.add_card(Card(2))
        hand.add_card(Card(5))
        hand.add_card(Card(11))

        # For even count, Hand.mid() picks the lower-middle (index (n-1)//2)
        card = Action.to_card(Action.MEDIUM, hand)

        self.assertEqual(card, Card(5))

    def test_higher_returns_max_card(self):
        hand = Hand()
        hand.add_card(Card(4))
        hand.add_card(Card(9))
        hand.add_card(Card(6))

        card = Action.to_card(Action.HIGHER, hand)

        self.assertEqual(card, Card(9))

    def test_invalid_action_raises_value_error(self):
        hand = Hand()
        hand.add_card(Card(1))

        with self.assertRaises(ValueError):
            Action.to_card("X", hand)

    def test_empty_hand_returns_none_for_any_action(self):
        hand = Hand()

        self.assertIsNone(Action.to_card(Action.LOWER, hand))
        self.assertIsNone(Action.to_card(Action.MEDIUM, hand))
        self.assertIsNone(Action.to_card(Action.HIGHER, hand))

    def test_get_all_actions(self):
        actions = Action.get_all_actions()
        self.assertSetEqual(set(actions), {Action.LOWER, Action.MEDIUM, Action.HIGHER})


if __name__ == '__main__':
    unittest.main()
