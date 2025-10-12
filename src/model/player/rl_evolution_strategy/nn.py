import numpy as np

from src.model.player.rl_evolution_strategy.action import ActionType
from src.model.player.rl_evolution_strategy.state import StateType


def softmax(a):
    c = np.max(a, axis=1, keepdims=True)
    e = np.exp(a - c)
    return e / e.sum(axis=-1, keepdims=True)


def relu(x):
    return x * (x > 0)


class ANN:
    def __init__(self, input_size: int, hidden_size: int, output_size: int, activation_function=relu, seed: int = 42):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.activation_function = activation_function

        self.generator = np.random.default_rng(seed=seed)

        self.W1 = None
        self.b1 = None
        self.W2 = None
        self.b2 = None

    def init(self):
        self.W1 = self.generator.standard_normal(size=(self.input_size, self.hidden_size)) / np.sqrt(self.input_size)
        self.b1 = np.zeros(self.hidden_size)
        self.W2 = self.generator.standard_normal(size=(self.hidden_size, self.output_size)) / np.sqrt(self.hidden_size)
        self.b2 = np.zeros(self.output_size)

    def forward(self, X):
        Z = self.activation_function(X.dot(self.W1) + self.b1)
        return softmax(Z.dot(self.W2) + self.b2)

    def sample_action(self, x: StateType) -> ActionType:
        # assume input is a single state of size (input_size,)
        # first make it (N, input_size) to fit ML conventions
        X = np.atleast_2d(x)
        P = self.forward(X)
        p = P[0]  # the first row
        return p

    def mutate(self, mutation: np.ndarray) -> "ANN":
        current_params = self.get_params()
        params_try = current_params + mutation
        mutated_nn = ANN(self.input_size, self.hidden_size, self.output_size)
        mutated_nn.set_params(params_try)
        return mutated_nn

    def update(self, update: np.ndarray) -> None:
        current_params = self.get_params()
        new_params = current_params + update
        self.set_params(new_params)

    def copy(self) -> "ANN":
        nn_copy = ANN(self.input_size, self.hidden_size, self.output_size)
        nn_copy.W1 = np.copy(self.W1)
        nn_copy.b1 = np.copy(self.b1)
        nn_copy.W2 = np.copy(self.W2)
        nn_copy.b2 = np.copy(self.b2)
        return nn_copy

    def get_params(self):
        # return a flat array of parameters
        return np.concatenate([self.W1.flatten(), self.b1, self.W2.flatten(), self.b2])

    def get_params_dict(self):
        return {
            'W1': self.W1,
            'b1': self.b1,
            'W2': self.W2,
            'b2': self.b2,
        }

    def set_params(self, params: np.ndarray) -> None:
        # params is a flat list
        # unflatten into individual weights
        D, M, K = self.input_size, self.hidden_size, self.output_size
        self.W1 = params[:D * M].reshape(D, M)
        self.b1 = params[D * M:D * M + M]
        self.W2 = params[D * M + M:D * M + M + M * K].reshape(M, K)
        self.b2 = params[-K:]

    def save(self, file_path: str) -> None:
        np.savez(
            file_path,
            **self.get_params_dict(),
        )

    @classmethod
    def load(cls, file_path: str) -> "ANN":
        saved_params = np.load(file_path)
        W1 = saved_params['W1']
        b1 = saved_params['b1']
        W2 = saved_params['W2']
        b2 = saved_params['b2']
        input_size = W1.shape[0]
        hidden_size = W1.shape[1]
        output_size = W2.shape[1]
        ann = cls(input_size, hidden_size, output_size)
        ann.W1 = W1
        ann.b1 = b1
        ann.W2 = W2
        ann.b2 = b2
        return ann
