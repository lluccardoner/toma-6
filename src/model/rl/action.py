from typing import List, Tuple

from src.model.card import Card
from src.model.hand import Hand

ActionType = Tuple[str]

class Action:
    LOWER = ("L",)
    MEDIUM = ("M",)
    HIGHER = ("H",)

    @classmethod
    def get_all_actions(cls) -> List[ActionType]:
        return [cls.LOWER, cls.MEDIUM, cls.HIGHER]

    @classmethod
    def to_card(cls, a: ActionType, hand: Hand) -> Card:
        if a == cls.LOWER:
            return hand.min()
        elif a == cls.MEDIUM:
            return hand.mid()
        elif a == cls.HIGHER:
            return hand.max()
        else:
            raise ValueError(f"Invalid action: {a}")
