class Card:
    def __init__(self, value):
        self.value = value
        self.points = self.calculate_points()

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
