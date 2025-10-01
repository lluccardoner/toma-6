import json
import os
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from src.model.rl.action import Action
from src.model.rl.state import State

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


def save_Q_to_file(Q: Dict[Any, Dict[Any, float]], path: str, player_name: str) -> str:
    output_file = os.path.join(path, f"Q_{player_name}.json")
    output_file_sanitized = output_file.replace(" ", "_")
    Q_sanitized = {str(s): {str(a): v for a, v in a_dict.items()} for s, a_dict in Q.items()}
    with open(output_file_sanitized, "w", encoding="utf-8") as f:
        json.dump(Q_sanitized, f)
    return output_file_sanitized


def load_Q_from_file(file_path: str) -> Dict[Any, Dict[Any, float]]:
    with open(file_path, "r", encoding="utf-8") as f:
        Q_loaded = json.load(f)
    Q = {eval(s): {eval(a): v for a, v in a_dict.items()} for s, a_dict in Q_loaded.items()}
    return Q


# def plot_Q_to_file(Q: Dict[Any, Dict[Any, float]], path: str, player_name: str) -> None:
#     output_file = os.path.join(path, f"Q_{player_name}.png")
#     output_file_sanitized = output_file.replace(" ", "_")
#
#     states = State.get_all_states()
#     actions = Action.get_all_actions()
#     Q_matrix = np.array([[Q[s][a] for a in actions] for s in states])
#
#     fig = plt.figure(figsize=(10, 20))
#     sns.heatmap(Q_matrix, xticklabels=actions, yticklabels=states, cmap="viridis")
#     plt.title(f"Q-values Heatmap")
#     plt.xlabel("Actions")
#     plt.ylabel("States")
#     plt.savefig(output_file_sanitized, dpi=300, bbox_inches="tight")
#     plt.close(fig)

import os
from typing import Any, Dict, Iterable, Sequence, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def plot_Q_to_file(
    Q: Dict[Any, Dict[Any, float]],
    path: str,
    player_name: str,
    dims: Tuple[int, int] = (0, 1),                # which two state dims to show (x, y)
    agg: str = "mean",                              # "mean" | "median" | "max" | "min"
    action_order: Sequence[Any] = ("L", "M", "H"),  # order to display actions
    tick_cap: int = 20                              # max ticks per axis (avoid clutter)
) -> None:
    """
    Render three heatmaps (one per action) of Q(s,a):
    - X/Y axes are two chosen state dimensions (dims)
    - Remaining state dimensions are aggregated using `agg`
    - Single figure, shared colorbar & colormap
    """
    # --- Gather states & actions ---
    states: Iterable[Any] = State.get_all_states()
    actions: Sequence[Any] = list(Action.get_all_actions())

    # Harmonize action order with whatever Action returns
    action_order = [a for a in action_order if a in actions]
    if len(action_order) == 0:
        raise ValueError("No overlap between provided action_order and available actions.")
    # If there are extra actions not in action_order, append them to the end
    action_order += [a for a in actions if a not in action_order]

    # Convert to arrays we can index
    states_list = list(states)
    try:
        states_arr = np.array([tuple(s) for s in states_list], dtype=object)  # (N, 4)
    except Exception as e:
        raise ValueError("States must be 4-tuples (iterables of length 4).") from e
    if states_arr.ndim != 2 or states_arr.shape[1] != 4:
        raise ValueError(f"Expected states as (N,4), got {states_arr.shape}")

    # Values array: (N, A)
    try:
        values_arr = np.array([[Q[s][a] for a in action_order] for s in states_list], dtype=float)
    except KeyError as e:
        missing = str(e)
        raise KeyError(f"Missing Q entry for state/action: {missing}") from e

    # --- Choose axes and build bins ---
    d_x, d_y = dims
    if not (0 <= d_x < 4 and 0 <= d_y < 4 and d_x != d_y):
        raise ValueError("`dims` must pick two distinct indices from {0,1,2,3}.")

    xs = np.unique(states_arr[:, d_x])
    ys = np.unique(states_arr[:, d_y])

    # Map axis values to indices
    x_to_ix = {v: i for i, v in enumerate(xs)}
    y_to_iy = {v: i for i, v in enumerate(ys)}
    xi = np.vectorize(x_to_ix.get)(states_arr[:, d_x])
    yi = np.vectorize(y_to_iy.get)(states_arr[:, d_y])

    # --- Aggregate over the remaining state dims ---
    Z = np.full((len(action_order), len(ys), len(xs)), np.nan, dtype=float)

    # Precompute masks per cell for speed if grid is large
    # (Iterating is fine for 14641 cells; we keep it clear & correct.)
    for ix in range(len(xs)):
        for iy in range(len(ys)):
            mask = (xi == ix) & (yi == iy)
            if not np.any(mask):
                continue
            block = values_arr[mask, :]  # (n, A)
            if agg == "mean":
                Z[:, iy, ix] = np.nanmean(block, axis=0)
            elif agg == "median":
                Z[:, iy, ix] = np.nanmedian(block, axis=0)
            elif agg == "max":
                Z[:, iy, ix] = np.nanmax(block, axis=0)
            elif agg == "min":
                Z[:, iy, ix] = np.nanmin(block, axis=0)
            else:
                raise ValueError(f"Unknown agg: {agg}")

    # Shared color scale across actions
    vmin = np.nanmin(Z)
    vmax = np.nanmax(Z)
    if not np.isfinite(vmin) or not np.isfinite(vmax):
        raise ValueError("All Z values are NaN/inf; cannot plot.")

    # Colormap with a distinct 'bad' color for NaNs
    cmap = mpl.cm.get_cmap("viridis").copy()
    cmap.set_bad("lightgray", alpha=0.6)

    # --- Plot: three panels, shared colorbar ---
    fig, axes = plt.subplots(1, len(action_order), figsize=(4.5 * len(action_order), 10), constrained_layout=True)
    if len(action_order) == 1:
        axes = [axes]  # ensure iterable

    ims = []
    for a_idx, a in enumerate(action_order):
        ax = axes[a_idx]
        im = ax.imshow(Z[a_idx], origin="lower", aspect="auto", vmin=vmin, vmax=vmax, cmap=cmap)
        ims.append(im)
        ax.set_title(f"Action: {a}")
        ax.set_xlabel(f"State dim {d_x}")
        if a_idx == 0:
            ax.set_ylabel(f"State dim {d_y}")

        # Optional tick labels (avoid overcrowding)
        if len(xs) <= tick_cap:
            ax.set_xticks(range(len(xs)))
            ax.set_xticklabels(xs, rotation=90)
        else:
            ax.set_xticks([])

        if len(ys) <= tick_cap:
            ax.set_yticks(range(len(ys)))
            ax.set_yticklabels(ys)
        else:
            ax.set_yticks([])

    # One shared colorbar
    # Use the first image as mappable; attach to all axes
    cbar = fig.colorbar(ims[0], ax=axes, fraction=0.03, pad=0.02)
    cbar.set_label("Q-value")

    # Save
    output_file = os.path.join(path, f"Q_{player_name}.png")
    output_file_sanitized = output_file.replace(" ", "_")
    plt.suptitle("Q-values Heatmaps (shared scale)", y=1.02)
    plt.savefig(output_file_sanitized, dpi=300, bbox_inches="tight")
    plt.close(fig)