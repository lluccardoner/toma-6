from typing import Dict

from src.model.card import Card

# Round -> Turn -> Player name -> Card
ChosenCardsHistoryType = Dict[int, Dict[int, Dict[str, Card]]]
