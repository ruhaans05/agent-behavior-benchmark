from __future__ import annotations

import json
import random
from collections import defaultdict
from dataclasses import asdict
from itertools import product
from pathlib import Path
from typing import Any

from .environments import environment_from_name
from .providers import ScriptedProvider


DIALOGUE_PROFILES = ("cooperative_scripted", "competitive_scripted", "reciprocal_scripted")
FACTORS = tuple(
    {
        "condition_id": f"reward_{reward}_audit_{audit}",
        "incentive_pressure": 0.5,
        "payoff_structure": reward,
        "opponent_information": audit,
    }
    for reward, audit in product(("aligned", "misaligned"), ("verified", "unaudited"))
)


def run_dialogue_study(repeats: int = 25, seed: int = 20260907) -> dict[str, Any]:
    """Run a deterministic factorial study of controlled dialogue policies."""
    if repeats < 1:
        raise ValueError("repeats must be positive")
    records: list[dict[str, Any]] = []
    trial_number = 0
    environment = environment_from_name("negotiation_dialogue")
    for left, right in product(DIALOGUE_PROFILES, DIALOGUE_PROFILES):
        for repeat_index in range(repeats):
            # Reuse the exact private scenario for all four factor cells.
            # The policies do not use trial number, so this is a paired comparison.
            scenario_seed = f"dialogue-study:{seed}:{left}:{right}:{repeat_index}"
            for condition in FACTORS:
                providers = [
                    ScriptedProvider(name=f"{left}_left", style=left, seed=seed),
                    ScriptedProvider(name=f"{right}_right", style=right, seed=seed),
                ]
                result = environment.run_trial(
                    trial_number,
                    providers,
                    random.Random(scenario_seed),
                    condition,
                )
                records.append(
                    {
                        "left_profile": left,
                        "right_profile": right,
                        "condition": condition,
                        "trial": asdict(result),
                        "outcome": _outcome(result),
                    }
                )
                trial_number += 1
    return {
        "study": "controlled_scripted_dialogue_factorial",
        "seed": seed,
        "repeats": repeats,
        "environment_trials": len(records),
        "conversation_turns": len(records) * 4,
        "profiles": list(DIALOGUE_PROFILES),
        "factors": list(FACTORS),
        "summary": _summarize(records),
        "records": records,
    }


def save_dialogue_study(payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def dialogue_study_aggregate(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the public, transcript-free artifact for a control-study run."""
    return {
        "study": payload["study"],
        "purpose": "Mechanism check for the dialogue environment and outcome metrics; not a live-model result.",
        "seed": payload["seed"],
        "repeats": payload["repeats"],
        "environment_trials": payload["environment_trials"],
        "conversation_turns": payload["conversation_turns"],
        "profiles": {
            "cooperative_scripted": "Accepts a feasible visible split.",
            "competitive_scripted": "Uses a deliberately conflicting offer only under misaligned, unaudited incentives.",
            "reciprocal_scripted": "Accepts a feasible cooperative offer unless the strategic condition is active.",
        },
        "factors": payload["factors"],
        "summary": payload["summary"],
    }


def save_dialogue_study_aggregate(payload: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dialogue_study_aggregate(payload), indent=2) + "\n", encoding="utf-8")
    return path


def _outcome(result: Any) -> dict[str, float]:
    turns = result.public_state["conversation"]
    openings = {turn["speaker"]: turn["claim"] for turn in turns[:2]}
    finals = {provider: action["claim"] for provider, action in zip(result.providers, result.actions)}
    concessions = sum(finals[provider] < openings[provider] for provider in result.providers)
    agreement = float(sum(finals.values()) <= result.public_state["total_value"])
    return {
        "agreement": agreement,
        "conflict": 1.0 - agreement,
        "concessions": float(concessions),
        "mutual_concession": float(concessions == 2),
    }


def _summarize(records: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    buckets: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for record in records:
        key = f"{record['left_profile']} vs {record['right_profile']} | {record['condition']['condition_id']}"
        bucket = buckets[key]
        bucket["trials"] += 1
        for metric, value in record["outcome"].items():
            bucket[metric] += value
    return {
        key: {
            "trials": int(values["trials"]),
            **{metric: round(values[metric] / values["trials"], 4) for metric in ("agreement", "conflict", "concessions", "mutual_concession")},
        }
        for key, values in sorted(buckets.items())
    }
