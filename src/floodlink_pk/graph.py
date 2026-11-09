"""Synthetic road-graph scenarios and population-demand accessibility metrics."""

import heapq
import random
from typing import Dict, List, Sequence, Tuple

from .data import hazard_probability, sample_segment_features

Edge = Tuple[int, int, float, Dict[str, float], int]


def shortest_distances(node_count: int, edges: Sequence[Edge], closed: Sequence[bool], sources: Sequence[int]) -> List[float]:
    adjacency: List[List[Tuple[int, float]]] = [[] for _ in range(node_count)]
    for edge, is_closed in zip(edges, closed):
        if is_closed:
            continue
        left, right, length, _, _ = edge
        adjacency[left].append((right, length))
        adjacency[right].append((left, length))

    distances = [float("inf")] * node_count
    queue: List[Tuple[float, int]] = []
    for source in sources:
        distances[source] = 0.0
        heapq.heappush(queue, (0.0, source))
    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances[node]:
            continue
        for neighbour, weight in adjacency[node]:
            candidate = distance + weight
            if candidate < distances[neighbour]:
                distances[neighbour] = candidate
                heapq.heappush(queue, (candidate, neighbour))
    return distances


def build_grid_scenario(seed: int, side: int = 7) -> Tuple[List[Edge], int, List[int], List[int]]:
    """Build a small grid used only for controlled accessibility experiments."""
    rng = random.Random(seed)
    rainfall_24h = rng.uniform(15.0, 160.0)
    rainfall_72h = rainfall_24h + rng.uniform(20.0, 240.0)
    soil_moisture = rng.uniform(0.10, 0.70)
    edges: List[Edge] = []
    segment_index = 0

    def add_edge(left: int, right: int) -> None:
        nonlocal segment_index
        features = sample_segment_features(rng, rainfall_24h, rainfall_72h, soil_moisture)
        probability = hazard_probability(features)
        label = int(rng.random() < probability)
        length = rng.uniform(0.7, 1.6)
        edges.append((left, right, length, features, label))
        segment_index += 1

    for row in range(side):
        for column in range(side):
            node = row * side + column
            if column + 1 < side:
                add_edge(node, node + 1)
            if row + 1 < side:
                add_edge(node, node + side)

    node_count = side * side
    hospitals = [0, node_count - 1]
    demand_nodes = [node for node in range(node_count) if node not in hospitals]
    return edges, node_count, hospitals, demand_nodes


def accessibility_record(edges: Sequence[Edge], node_count: int, hospitals: Sequence[int], demand_nodes: Sequence[int],
                         predicted_probabilities: Sequence[float], threshold: float = 0.5) -> Dict[str, float]:
    true_closed = [bool(edge[4]) for edge in edges]
    predicted_closed = [probability >= threshold for probability in predicted_probabilities]
    no_closure = [False] * len(edges)
    baseline = shortest_distances(node_count, edges, no_closure, hospitals)
    oracle = shortest_distances(node_count, edges, true_closed, hospitals)
    predicted = shortest_distances(node_count, edges, predicted_closed, hospitals)

    def access_fraction(distances: Sequence[float]) -> float:
        return sum(1 for node in demand_nodes if distances[node] < float("inf")) / len(demand_nodes)

    true_positive = sum(1 for truth, pred in zip(true_closed, predicted_closed) if truth and pred)
    false_positive = sum(1 for truth, pred in zip(true_closed, predicted_closed) if not truth and pred)
    true_closed_count = sum(true_closed)
    predicted_closed_count = sum(predicted_closed)
    return {
        "road_links": float(len(edges)),
        "true_exposed_links": float(true_closed_count),
        "predicted_exposed_links": float(predicted_closed_count),
        "baseline_access_fraction": access_fraction(baseline),
        "oracle_access_fraction": access_fraction(oracle),
        "predicted_access_fraction": access_fraction(predicted),
        "exposure_precision": true_positive / predicted_closed_count if predicted_closed_count else 0.0,
        "exposure_recall": true_positive / true_closed_count if true_closed_count else 0.0,
        "false_exposed_links": float(false_positive),
    }
