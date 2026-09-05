from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable


TOKEN_PATTERN = re.compile(r"[a-z0-9_]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


@dataclass
class BinaryNaiveBayes:
    """Small dependency-free text classifier for labeled synthetic action traces."""

    alpha: float = 1.0

    def fit(self, examples: Iterable[tuple[str, bool]]) -> "BinaryNaiveBayes":
        self.document_counts = Counter({False: 0, True: 0})
        self.token_counts = {False: Counter(), True: Counter()}
        self.token_totals = Counter({False: 0, True: 0})
        self.vocabulary: set[str] = set()

        for text, label in examples:
            tokens = tokenize(text)
            self.document_counts[label] += 1
            self.token_counts[label].update(tokens)
            self.token_totals[label] += len(tokens)
            self.vocabulary.update(tokens)

        if not self.document_counts[True] or not self.document_counts[False]:
            raise ValueError("Each classifier needs positive and negative training examples.")
        return self

    def predict(self, text: str) -> bool:
        scores = self._log_scores(text)
        return scores[True] >= scores[False]

    def _log_scores(self, text: str) -> dict[bool, float]:
        total_documents = sum(self.document_counts.values())
        vocabulary_size = max(1, len(self.vocabulary))
        scores: dict[bool, float] = {}

        for label in (False, True):
            prior = self.document_counts[label] / total_documents
            score = math.log(prior)
            denominator = self.token_totals[label] + self.alpha * vocabulary_size
            for token in tokenize(text):
                numerator = self.token_counts[label][token] + self.alpha
                score += math.log(numerator / denominator)
            scores[label] = score
        return scores


def binary_metrics(predictions: Iterable[tuple[bool, bool]]) -> dict[str, float | int]:
    pairs = list(predictions)
    true_positive = sum(predicted and actual for predicted, actual in pairs)
    false_positive = sum(predicted and not actual for predicted, actual in pairs)
    false_negative = sum(not predicted and actual for predicted, actual in pairs)
    support = sum(actual for _, actual in pairs)

    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    accuracy = sum(predicted == actual for predicted, actual in pairs) / len(pairs) if pairs else 0.0
    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "support": support,
        "test_examples": len(pairs),
    }
