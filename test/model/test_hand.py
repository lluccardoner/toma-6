import unittest

from src.model.card import Card
from src.model.hand import Hand


class TestHand(unittest.TestCase):

    def test_add_card(self):
        # Arrange
        hand = Hand()
        card = Card(value=5)

        # Act
        hand.add_card(card)

        # Assert
        self.assertIn(card, hand.cards)

    def test_pop_card_by_value(self):
        # Arrange
        hand = Hand()
        card1 = Card(value=5)
        card2 = Card(value=10)
        hand.add_card(card1)
        hand.add_card(card2)

        # Act
        popped_card = hand.pop_card_by_value(5)

        # Assert
        self.assertEqual(popped_card, card1)
        self.assertNotIn(card1, hand.cards)
        self.assertIn(card2, hand.cards)

    def test_pop_card_by_index(self):
        # Arrange
        hand = Hand()
        card1 = Card(value=5)
        card2 = Card(value=10)
        hand.add_card(card1)
        hand.add_card(card2)

        # Act
        popped_card = hand.pop_card_by_index(0)

        # Assert
        self.assertEqual(popped_card, card1)
        self.assertNotIn(card1, hand.cards)
        self.assertIn(card2, hand.cards)

    def test_reset(self):
        # Arrange
        hand = Hand()
        card = Card(value=5)
        hand.add_card(card)

        # Act
        hand.reset()

        # Assert
        self.assertEqual(len(hand.cards), 0)

    def test_sort(self):
        # Arrange
        hand = Hand()
        card1 = Card(value=10)
        card2 = Card(value=5)
        hand.add_card(card1)
        hand.add_card(card2)

        # Act
        hand.sort()

        # Assert
        self.assertEqual(hand.cards[0], card2)
        self.assertEqual(hand.cards[1], card1)

    def test_len(self):
        # Arrange
        hand = Hand()
        card1 = Card(value=5)
        card2 = Card(value=10)
        hand.add_card(card1)
        hand.add_card(card2)

        # Act
        length = len(hand)

        # Assert
        self.assertEqual(length, 2)

    def test_iter(self):
        # Arrange
        hand = Hand()
        card1 = Card(value=5)
        card2 = Card(value=10)
        hand.add_card(card1)
        hand.add_card(card2)

        # Act
        cards = list(iter(hand))

        # Assert
        self.assertEqual(cards, [card1, card2])

    def test_str(self):
        # Arrange
        hand = Hand()
        card1 = Card(value=5)
        card2 = Card(value=10)
        hand.add_card(card1)
        hand.add_card(card2)

        # Act
        string = str(hand)

        # Assert
        self.assertEqual(string, "[5, 10]")

    def test_rpr(self):
        # Arrange
        hand = Hand()
        card1 = Card(value=5)
        card2 = Card(value=10)
        hand.add_card(card1)
        hand.add_card(card2)

        # Act
        string = repr(hand)

        # Assert
        self.assertEqual(string, "Hand([5, 10])")


if __name__ == '__main__':
    unittest.main()
