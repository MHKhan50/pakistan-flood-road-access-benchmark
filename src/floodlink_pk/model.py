"""Small dependency-free multilayer perceptron for link exposure classification."""

import math
import random
from typing import Dict, List, Sequence, Tuple

from .data import FEATURE_COLUMNS, feature_vector


def _sigmoid(value: float) -> float:
    value = max(-35.0, min(35.0, value))
    return 1.0 / (1.0 + math.exp(-value))


class Standardizer:
    """Feature standardizer fitted on training data only."""

    def __init__(self) -> None:
        self.means: List[float] = []
        self.scales: List[float] = []

    def fit(self, rows: Sequence[Dict[str, float]]) -> None:
        if not rows:
            raise ValueError("Cannot fit standardizer on an empty dataset")
        vectors = [feature_vector(row) for row in rows]
        width = len(FEATURE_COLUMNS)
        self.means = [sum(vector[i] for vector in vectors) / len(vectors) for i in range(width)]
        self.scales = []
        for index in range(width):
            variance = sum((vector[index] - self.means[index]) ** 2 for vector in vectors) / len(vectors)
            self.scales.append(math.sqrt(variance) or 1.0)

    def transform(self, values: Sequence[float]) -> List[float]:
        if not self.means or not self.scales:
            raise RuntimeError("Standardizer has not been fitted")
        return [(float(value) - mean) / scale for value, mean, scale in zip(values, self.means, self.scales)]


class TinyMLP:
    """One-hidden-layer MLP trained with stochastic gradient descent.

    This implementation intentionally uses only the Python standard library.
    It is a reproducibility baseline, not a production geospatial model.
    """

    def __init__(
        self,
        input_size: int = len(FEATURE_COLUMNS),
        hidden_size: int = 10,
        seed: int = 17,
        learning_rate: float = 0.025,
        l2: float = 0.0005,
    ) -> None:
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate
        self.l2 = l2
        self.rng = random.Random(seed)
        scale = 1.0 / math.sqrt(input_size)
        self.weights_in = [
            [self.rng.uniform(-scale, scale) for _ in range(input_size)]
            for _ in range(hidden_size)
        ]
        self.bias_hidden = [0.0 for _ in range(hidden_size)]
        self.weights_out = [self.rng.uniform(-0.25, 0.25) for _ in range(hidden_size)]
        self.bias_out = 0.0
        self.standardizer = Standardizer()
        self.is_fitted = False

    def _forward(self, values: Sequence[float]) -> Tuple[List[float], float]:
        hidden = []
        for weights, bias in zip(self.weights_in, self.bias_hidden):
            activation = bias + sum(weight * value for weight, value in zip(weights, values))
            hidden.append(math.tanh(activation))
        output = _sigmoid(self.bias_out + sum(weight * value for weight, value in zip(self.weights_out, hidden)))
        return hidden, output

    def fit(self, rows: Sequence[Dict[str, float]], epochs: int = 55) -> "TinyMLP":
        if not rows:
            raise ValueError("Cannot train on an empty dataset")
        if epochs < 1:
            raise ValueError("epochs must be positive")
        self.standardizer.fit(rows)
        prepared = [
            (self.standardizer.transform(feature_vector(row)), float(row["flood_exposed"]))
            for row in rows
        ]
        indices = list(range(len(prepared)))
        for _ in range(epochs):
            self.rng.shuffle(indices)
            for index in indices:
                values, target = prepared[index]
                hidden, prediction = self._forward(values)
                output_gradient = prediction - target
                previous_output_weights = list(self.weights_out)
                hidden_gradients = [
                    output_gradient * previous_output_weights[j] * (1.0 - hidden[j] * hidden[j])
                    for j in range(self.hidden_size)
                ]
                self.bias_out -= self.learning_rate * output_gradient
                for j in range(self.hidden_size):
                    self.weights_out[j] -= self.learning_rate * (
                        output_gradient * hidden[j] + self.l2 * self.weights_out[j]
                    )
                for j in range(self.hidden_size):
                    self.bias_hidden[j] -= self.learning_rate * hidden_gradients[j]
                    for k in range(self.input_size):
                        gradient = hidden_gradients[j] * values[k] + self.l2 * self.weights_in[j][k]
                        self.weights_in[j][k] -= self.learning_rate * gradient
        self.is_fitted = True
        return self

    def predict_proba(self, rows: Sequence[Dict[str, float]]) -> List[float]:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction")
        probabilities = []
        for row in rows:
            values = self.standardizer.transform(feature_vector(row))
            _, probability = self._forward(values)
            probabilities.append(probability)
        return probabilities

    def predict(self, rows: Sequence[Dict[str, float]], threshold: float = 0.5) -> List[int]:
        return [int(probability >= threshold) for probability in self.predict_proba(rows)]
