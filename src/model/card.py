class Card:
    def __init__(self, value):
        self.value = value
        self.points = self.calculate_points()

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'Card({self.value})'

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def calculate_points(self):
        if self.value % 5 == 0 and self.value % 11 == 0:
            return 7
        elif self.value % 11 == 0:
            return 5
        elif self.value % 10 == 0:
            return 3
        elif self.value % 5 == 0:
            return 2
        else:
            return 1
