"""Classification and probability-quality metrics."""

from typing import Dict, Sequence


def classification_metrics(labels: Sequence[int], probabilities: Sequence[float], threshold: float = 0.5) -> Dict[str, float]:
    if len(labels) != len(probabilities) or not labels:
        raise ValueError("labels and probabilities must have the same non-zero length")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")
    predictions = [int(probability >= threshold) for probability in probabilities]
    tp = sum(1 for truth, pred in zip(labels, predictions) if truth == 1 and pred == 1)
    tn = sum(1 for truth, pred in zip(labels, predictions) if truth == 0 and pred == 0)
    fp = sum(1 for truth, pred in zip(labels, predictions) if truth == 0 and pred == 1)
    fn = sum(1 for truth, pred in zip(labels, predictions) if truth == 1 and pred == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = (tp + tn) / len(labels)
    brier = sum((probability - truth) ** 2 for truth, probability in zip(labels, probabilities)) / len(labels)

    positives = sum(labels)
    negatives = len(labels) - positives
    if positives and negatives:
        ordered = sorted(zip(probabilities, labels), key=lambda item: item[0])
        rank_sum = 0.0
        index = 0
        while index < len(ordered):
            end = index + 1
            while end < len(ordered) and ordered[end][0] == ordered[index][0]:
                end += 1
            average_rank = ((index + 1) + end) / 2.0
            rank_sum += average_rank * sum(label for _, label in ordered[index:end])
            index = end
        auc = (rank_sum - positives * (positives + 1) / 2.0) / (positives * negatives)
    else:
        auc = 0.5

    bins = 10
    calibration_error = 0.0
    for bin_index in range(bins):
        lower = bin_index / bins
        upper = (bin_index + 1) / bins
        members = [
            (truth, probability)
            for truth, probability in zip(labels, probabilities)
            if lower <= probability < upper or (bin_index == bins - 1 and probability == 1.0)
        ]
        if members:
            average_confidence = sum(probability for _, probability in members) / len(members)
            average_accuracy = sum(truth for truth, _ in members) / len(members)
            calibration_error += len(members) / len(labels) * abs(average_confidence - average_accuracy)

    return {
        "n": float(len(labels)),
        "threshold": threshold,
        "positive_rate": positives / len(labels),
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": auc,
        "brier_score": brier,
        "expected_calibration_error_10_bins": calibration_error,
    }
