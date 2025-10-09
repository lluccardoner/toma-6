from typing import Optional

from src.model.player.rl_evolution_strategy.action import Action
from src.model.player.rl_evolution_strategy.nn import ANN
from src.model.player.rl_evolution_strategy.state import State
from src.model.board import Board
from src.model.card import Card
from src.model.game_history import GameHistory
from src.model.hand import Hand
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy


class RLEvolutionStrategyChooseCardStrategy(BaseChooseCardStrategy):
    def __init__(self, policy_nn: Optional[ANN] = None):
        if policy_nn:
            self.policy_nn: ANN = policy_nn
        else:
            self.policy_nn: ANN = ANN(
                input_size=State.number_states,
                hidden_size=100,
                output_size=Action.number_actions
            )
            self.policy_nn.init()

    def choose_card(
            self,
            hand: Hand,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None,
            game_history: Optional[GameHistory] = None
    ) -> Card:
        s = State.create(board, hand)
        a = self.policy_nn.sample_action(s)
        card = Action.to_card(a, hand)
        return card
