import unittest
from src.model.card_deck import CardDeck
from src.model.card import Card

class TestCardDeck(unittest.TestCase):

    def test_initial_deck_size(self):
        # Arrange
        deck = CardDeck()

        # Act
        initial_size = len(deck.cards)

        # Assert
        self.assertEqual(initial_size, 104)

    def test_shuffle_changes_order(self):
        # Arrange
        deck = CardDeck(seed=42)
        original_order = deck.cards.copy()

        # Act
        deck.shuffle()
        shuffled_order = deck.cards

        # Assert
        self.assertNotEqual(original_order, shuffled_order)

    def test_reset_restores_order(self):
        # Arrange
        deck = CardDeck(seed=42)
        deck.shuffle()

        # Act
        deck.reset()
        reset_order = deck.cards

        # Assert
        self.assertEqual(reset_order, [Card(i) for i in range(1, 105)])

    def test_reset_and_shuffle(self):
        # Arrange
        deck = CardDeck(seed=42)
        original_order = deck.cards.copy()

        # Act
        deck.reset_and_shuffle()
        reset_and_shuffled_order = deck.cards

        # Assert
        self.assertNotEqual(original_order, reset_and_shuffled_order)
        self.assertEqual(len(reset_and_shuffled_order), 104)

if __name__ == '__main__':
    unittest.main()