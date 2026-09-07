from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .environments import TrialResult
from .evaluators import score_action
from .live_study import LIVE_MODELS, _build_schedule


def analyze_live_trace(path: Path) -> dict[str, Any]:
    """Create aggregate, transcript-free results from a checkpointed live study."""
    records = _load_records(path)
    overall = _aggregate(records)
    by_structure = {
        structure: _aggregate([record for record in records if _structure(record) == structure])
        for structure in sorted({_structure(record) for record in records})
    }
    by_environment = {
        environment: _aggregate([record for record in records if record["trial"].experiment == environment])
        for environment in sorted({record["trial"].experiment for record in records})
    }
    return {
        "source": str(path),
        "completed_trials": len(records),
        "completed_agent_actions": len(records) * 2,
        "trial_coverage_by_condition": dict(sorted(Counter(record["cell"]["condition"]["condition_id"] for record in records).items())),
        "trial_coverage_by_pairing": dict(sorted(Counter(" vs ".join(record["trial"].providers) for record in records).items())),
        "models_returned": dict(sorted(Counter(
            action.get("_provenance", {}).get("returned_model", provider)
            for record in records
            for provider, action in zip(record["trial"].providers, record["trial"].actions)
        ).items())),
        "overall": overall,
        "by_payoff_structure": by_structure,
        "by_environment": by_environment,
    }


def save_live_analysis(payload: dict[str, Any], path: Path) -> Path:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def validate_live_trace(path: Path, phase: str, seed: int) -> dict[str, Any]:
    """Validate checkpoint continuity and protocol conformance without exposing transcripts."""
    records = _load_records(path)
    schedule = _build_schedule(phase, seed)
    issues: list[str] = []
    trial_ids = [record["trial"].trial for record in records]
    expected_ids = list(range(len(records)))
    if trial_ids != expected_ids:
        issues.append("checkpoint trial IDs are not contiguous from zero")
    if len(records) > len(schedule):
        issues.append("checkpoint contains more trials than the frozen schedule")

    for record in records:
        trial = record["trial"]
        if trial.trial >= len(schedule):
            continue
        expected_cell = schedule[trial.trial]
        if record["cell"] != expected_cell:
            issues.append(f"trial {trial.trial} does not match its frozen schedule cell")
        if trial.providers != [expected_cell["left"], expected_cell["right"]]:
            issues.append(f"trial {trial.trial} has unexpected provider order")
        if len(trial.actions) != 2:
            issues.append(f"trial {trial.trial} does not contain two actions")
            continue
        for action in trial.actions:
            provenance = action.get("_provenance", {})
            if not provenance.get("returned_model"):
                issues.append(f"trial {trial.trial} is missing a returned model ID")
                break

    return {
        "valid": not issues,
        "phase": phase,
        "seed": seed,
        "completed_trials": len(records),
        "scheduled_trials": len(schedule),
        "remaining_trials": max(0, len(schedule) - len(records)),
        "expected_models": list(LIVE_MODELS),
        "issues": issues,
    }


def _load_records(path: Path) -> list[dict[str, Any]]:
    by_trial: dict[int, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            trial = TrialResult(**record["trial"])
            cell = record["cell"]
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
        by_trial[trial.trial] = {"cell": cell, "trial": trial}
    return [by_trial[index] for index in sorted(by_trial)]


def _structure(record: dict[str, Any]) -> str:
    return str(record["cell"]["condition"].get("payoff_structure", "aligned"))


def _aggregate(records: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for record in records:
        trial = record["trial"]
        for provider, action in zip(trial.providers, trial.actions):
            for metric, value in score_action(action, trial.experiment).items():
                totals[provider][metric] += value
            totals[provider]["reward"] += trial.rewards.get(provider, 0.0)
            totals[provider]["actions"] += 1.0

    return {
        provider: {
            "actions": int(values["actions"]),
            **{metric: round(values[metric] / values["actions"], 4) for metric in ("deception", "collusion", "manipulation", "spec_gaming", "reward")},
        }
        for provider, values in sorted(totals.items())
    }
