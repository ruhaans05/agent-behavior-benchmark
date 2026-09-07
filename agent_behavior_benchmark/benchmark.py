from __future__ import annotations

import json
import random
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .environments import environment_from_name
from .evaluators import evaluate_trials
from .providers import provider_from_name

STARTER_EXPERIMENTS = ("negotiation", "resource_allocation", "auction")


def run_benchmark(
    experiment: str,
    provider_names: list[str],
    trials: int,
    seed: int,
    allow_live: bool = False,
    condition: dict[str, Any] | None = None,
) -> dict[str, Any]:
    names = list(STARTER_EXPERIMENTS) if experiment == "starter" else [experiment]
    rng = random.Random(seed)
    providers = [provider_from_name(name, seed=seed, allow_live=allow_live) for name in provider_names]

    results = []
    for name in names:
        environment = environment_from_name(name)
        for trial in range(trials):
            results.append(environment.run_trial(trial, providers, rng, condition))

    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "experiment": experiment,
        "providers": provider_names,
        "trials_per_environment": trials,
        "seed": seed,
        "condition": condition or {},
        "summary": evaluate_trials(results),
        "trials": [asdict(result) for result in results],
    }
    return payload


def save_run(payload: dict[str, Any], output_dir: Path = Path("runs")) -> Path:
    output_dir.mkdir(exist_ok=True)
    path = output_dir / f"{payload['experiment']}-{payload['seed']}-{_stamp()}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    latest = output_dir / "latest.json"
    latest.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def load_run(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
