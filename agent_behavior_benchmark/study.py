from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .benchmark import run_benchmark
from .classifiers import BinaryNaiveBayes, binary_metrics
from .evaluators import score_action


BEHAVIOR_LABELS = ("deception", "collusion", "spec_gaming")


def run_initial_study(trials_per_environment: int = 200, seed: int = 20260905) -> dict[str, Any]:
    """Run a deterministic simulated study with a trace-classification holdout."""
    benchmark = run_benchmark(
        experiment="starter",
        provider_names=["openai_style", "claude_style"],
        trials=trials_per_environment,
        seed=seed,
    )
    traces = _trace_records(benchmark["trials"])
    classifier_metrics = _evaluate_classifiers(traces)
    pressure_summary = _summarize_by_pressure(benchmark["trials"])

    return {
        "study": "initial_simulated_baseline",
        "study_scope": "synthetic, deterministic provider profiles; no live model calls",
        "seed": seed,
        "trials_per_environment": trials_per_environment,
        "environment_trials": len(benchmark["trials"]),
        "agent_actions": len(traces),
        "providers": benchmark["providers"],
        "aggregate_behavior_metrics": benchmark["summary"],
        "behavior_classifier_metrics": classifier_metrics,
        "incentive_pressure_summary": pressure_summary,
    }


def save_study(study: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(study, indent=2) + "\n", encoding="utf-8")
    return path


def _trace_records(trials: list[dict[str, Any]]) -> list[dict[str, Any]]:
    traces = []
    for trial in trials:
        for provider, action in zip(trial["providers"], trial["actions"]):
            scores = score_action(action)
            traces.append(
                {
                    "trial": trial["trial"],
                    "environment": trial["experiment"],
                    "provider": provider,
                    "pressure": float(trial["public_state"]["incentive_pressure"]),
                    "text": f"{action.get('message', '')} {action.get('rationale', '')}",
                    "labels": {label: bool(scores[label]) for label in BEHAVIOR_LABELS},
                }
            )
    return traces


def _evaluate_classifiers(traces: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    # Hold out every fifth per-environment trial so the split is reproducible.
    train = [trace for trace in traces if trace["trial"] % 5 != 0]
    test = [trace for trace in traces if trace["trial"] % 5 == 0]
    metrics = {}
    for label in BEHAVIOR_LABELS:
        classifier = BinaryNaiveBayes().fit((trace["text"], trace["labels"][label]) for trace in train)
        predictions = ((classifier.predict(trace["text"]), trace["labels"][label]) for trace in test)
        metrics[label] = binary_metrics(predictions)
    return metrics


def _summarize_by_pressure(trials: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, float]]]:
    totals: dict[str, dict[str, dict[str, float]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for trial in trials:
        pressure = str(trial["public_state"]["incentive_pressure"])
        for provider, action in zip(trial["providers"], trial["actions"]):
            scores = score_action(action)
            bucket = totals[provider][pressure]
            bucket["actions"] += 1
            for label in BEHAVIOR_LABELS:
                bucket[label] += scores[label]

    summary = {}
    for provider, by_pressure in totals.items():
        summary[provider] = {}
        for pressure, values in sorted(by_pressure.items()):
            n = values["actions"]
            summary[provider][pressure] = {
                "actions": int(n),
                **{label: round(values[label] / n, 4) for label in BEHAVIOR_LABELS},
            }
    return summary
