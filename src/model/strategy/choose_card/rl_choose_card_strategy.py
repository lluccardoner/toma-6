from typing import Optional, Dict, Any

from src.model.board import Board
from src.model.card import Card
from src.model.game_history import GameHistory
from src.model.hand import Hand
from src.model.rl.action import Action
from src.model.rl.rl_utils import init_Q, epsilon_greedy, max_dict, QValueType
from src.model.rl.state import State
from src.model.strategy.choose_card.base_choose_card_strategy import BaseChooseCardStrategy

ALL_STATES = State.get_all_states()
ALL_ACTIONS = Action.get_all_actions()


class RLChooseCardStrategyLearner(BaseChooseCardStrategy):
    def __init__(
            self,
            Q: Optional[QValueType] = None,
            epsilon: float = 0.1,
            alpha: float = 0.1,
            gamma: float = 0.9
    ):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.Q = Q or init_Q(ALL_STATES, ALL_ACTIONS)
        self.last_state = None
        self.last_action = None

    def choose_card(
            self,
            hand: Hand,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None,
            game_history: Optional[GameHistory] = None
    ) -> Card:
        # Perform an action based on the current state
        s = State.create(board)
        a = epsilon_greedy(self.Q, s, eps=self.epsilon, all_actions=ALL_ACTIONS)
        card = Action.to_card(a, hand)
        self.last_state = s
        self.last_action = a
        return card

    def update(
            self,
            reward: float,
            hand: Optional[Hand] = None,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None
    ) -> None:
        # Update the Q
        s = self.last_state
        a = self.last_action
        # Reward (points received) is positive but for the Q we use it negative since it is initialized to 0
        # If reward is 0, we give a small positive reward of 1
        r = -reward if reward > 0 else 1
        s2 = State.create(board)
        maxQ = max_dict(self.Q[s2])[1]
        self.Q[s][a] = self.Q[s][a] + self.alpha * (r + self.gamma * maxQ - self.Q[s][a])


class RLChooseCardStrategy(BaseChooseCardStrategy):
    def __init__(self, Q: QValueType):
        self.Q = Q

    def choose_card(
            self,
            hand: Hand,
            board: Optional[Board] = None,
            current_round: Optional[int] = None,
            current_turn: Optional[int] = None,
            game_history: Optional[GameHistory] = None
    ) -> Card:
        # Perform an action based on the current state
        s = State.create(board)
        a = max_dict(self.Q[s])[0]
        card = Action.to_card(a, hand)
        return card
