from typing import Tuple

import numpy as np

from src.model.card import Card
from src.model.hand import Hand

ActionType = np.ndarray


class Action:
    number_actions: int = 3
    dimensions: Tuple[int, ...] = (number_actions,)

    LOWER = 0
    MEDIUM = 1
    HIGHER = 2

    @classmethod
    def to_card(cls, a: ActionType, hand: Hand) -> Card:
        assert a.shape == cls.dimensions, f"Action shape {a.shape} does not match expected {cls.dimensions}"
        action = int(np.argmax(a))  # Convert one-hot to index
        if action == cls.LOWER:
            return hand.min()
        elif action == cls.MEDIUM:
            return hand.mid()
        elif action == cls.HIGHER:
            return hand.max()
        else:
            raise ValueError(f"Invalid action: {a}")
