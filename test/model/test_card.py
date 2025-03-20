import unittest

from src.model.card import Card


class TestCard(unittest.TestCase):

    def test_card_initialization(self):
        # Arrange
        value = 55

        # Act
        card = Card(value)

        # Assert
        self.assertEqual(card.value, value)
        self.assertEqual(card.points, 7)

    def test_card_str(self):
        # Arrange
        card = Card(5)

        # Act
        card_str = str(card)

        # Assert
        self.assertEqual(card_str, '5')

    def test_card_repr(self):
        # Arrange
        card = Card(5)

        # Act
        card_repr = repr(card)

        # Assert
        self.assertEqual(card_repr, 'Card(5)')

    def test_card_equality(self):
        # Arrange
        card1 = Card(5)
        card2 = Card(5)
        card3 = Card(10)

        # Act & Assert
        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)

    def test_card_comparison(self):
        # Arrange
        card1 = Card(5)
        card2 = Card(10)

        # Act & Assert
        self.assertTrue(card1 < card2)
        self.assertTrue(card2 > card1)

    def test_card_points(self):
        # Arrange & Act
        card1 = Card(5)
        card2 = Card(10)
        card3 = Card(11)
        card4 = Card(55)
        card5 = Card(1)

        # Assert
        self.assertEqual(card1.points, 2)
        self.assertEqual(card2.points, 3)
        self.assertEqual(card3.points, 5)
        self.assertEqual(card4.points, 7)
        self.assertEqual(card5.points, 1)

    if __name__ == '__main__':
        unittest.main()
