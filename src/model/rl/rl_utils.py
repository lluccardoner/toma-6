import json
import os
from typing import Any, Dict, List, Tuple

import numpy as np

from src.model.rl.action import ActionType
from src.model.rl.state import StateType

generator = np.random.default_rng(42)

QValueType = Dict[StateType, Dict[ActionType, float]]


def init_Q(states: List[StateType], actions: List[ActionType]) -> QValueType:
    # Initialize Q(s,a)
    Q = {}
    for s in states:
        Q[s] = {}
        for a in actions:
            Q[s][a] = 0
    return Q


def max_dict(d: Dict[ActionType, float]) -> Tuple[ActionType, float]:
    # returns the argmax (key) and max (value) from a dictionary
    max_val = max(d.values())
    max_keys = [k for k, v in d.items() if v == max_val]
    random_index = generator.choice(len(max_keys))
    return max_keys[random_index], max_val


def epsilon_greedy(Q: QValueType, s: StateType, eps: float, all_actions: List[Tuple]) -> Tuple:
    if generator.random() < eps:
        random_index = generator.choice(len(all_actions))
        return all_actions[random_index]
    else:
        return max_dict(Q[s])[0]


def save_Q_to_file(Q: QValueType, path: str, player_name: str) -> str:
    output_file = os.path.join(path, f"Q_{player_name}.json")
    output_file_sanitized = output_file.replace(" ", "_")
    Q_sanitized = {str(s): {str(a): v for a, v in a_dict.items()} for s, a_dict in Q.items()}
    with open(output_file_sanitized, "w", encoding="utf-8") as f:
        json.dump(Q_sanitized, f)
    return output_file_sanitized


def load_Q_from_file(file_path: str) -> QValueType:
    with open(file_path, "r", encoding="utf-8") as f:
        Q_loaded = json.load(f)
    Q = {eval(s): {eval(a): v for a, v in a_dict.items()} for s, a_dict in Q_loaded.items()}
    return Q
