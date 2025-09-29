from typing import Any, Dict, List, Tuple

import numpy as np

generator = np.random.default_rng(42)

def init_Q(states: List[Any], actions: List[Any]) -> Dict[Any, Dict[Any, float]]:
    # Initialize Q(s,a)
    Q = {}
    for s in states:
        Q[s] = {}
        for a in actions:
            Q[s][a] = 0
    return Q


def max_dict(d: Dict[Any, float]) -> Tuple[Any, float]:
    # returns the argmax (key) and max (value) from a dictionary
    max_val = max(d.values())
    max_keys = [k for k, v in d.items() if v == max_val]
    return generator.choice(max_keys), max_val


def epsilon_greedy(Q: Dict[Any, Dict[Any, float]], s: Any, eps: float, all_actions: List[Any]) -> Any:
    if generator.random() < eps:
        return generator.choice(all_actions)
    else:
        return max_dict(Q[s])[0]
