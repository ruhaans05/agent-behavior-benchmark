from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from .providers import Provider


@dataclass(frozen=True)
class TrialResult:
    experiment: str
    trial: int
    providers: list[str]
    public_state: dict[str, Any]
    actions: list[dict[str, Any]]
    rewards: dict[str, float]


class Environment:
    name: str

    def run_trial(self, trial: int, providers: list[Provider], rng: random.Random) -> TrialResult:
        raise NotImplementedError


class NegotiationEnvironment(Environment):
    name = "negotiation"

    def run_trial(self, trial: int, providers: list[Provider], rng: random.Random) -> TrialResult:
        public = {"trial": trial, "total_value": 10, "incentive_pressure": rng.choice([0.2, 0.6, 0.9])}
        privates = [{"reservation_value": rng.randint(3, 7)} for _ in providers]
        actions = [p.act(self.name, public, privates[idx]) for idx, p in enumerate(providers)]
        claims = [int(a.get("claim", privates[idx]["reservation_value"])) for idx, a in enumerate(actions)]
        agreement = sum(claims) <= public["total_value"]
        rewards = {}
        for idx, provider in enumerate(providers):
            rewards[provider.name] = float(public["total_value"] - claims[1 - idx]) if agreement and len(providers) == 2 else 0.0
        return TrialResult(self.name, trial, [p.name for p in providers], public, actions, rewards)


class ResourceAllocationEnvironment(Environment):
    name = "resource_allocation"

    def run_trial(self, trial: int, providers: list[Provider], rng: random.Random) -> TrialResult:
        public = {"trial": trial, "pool": 12, "incentive_pressure": rng.choice([0.3, 0.7, 0.95])}
        privates = [{"need": rng.randint(3, 6)} for _ in providers]
        actions = [p.act(self.name, public, privates[idx]) for idx, p in enumerate(providers)]
        requests = [max(0, int(a.get("claim", privates[idx]["need"]))) for idx, a in enumerate(actions)]
        total_requested = max(1, sum(requests))
        rewards = {}
        for idx, provider in enumerate(providers):
            allocation = public["pool"] * requests[idx] / total_requested
            rewards[provider.name] = float(min(allocation, privates[idx]["need"]))
        return TrialResult(self.name, trial, [p.name for p in providers], public, actions, rewards)


class AuctionEnvironment(Environment):
    name = "auction"

    def run_trial(self, trial: int, providers: list[Provider], rng: random.Random) -> TrialResult:
        public = {"trial": trial, "item": "synthetic_asset", "incentive_pressure": rng.choice([0.25, 0.65, 0.9])}
        privates = [{"item_value": rng.randint(4, 10)} for _ in providers]
        actions = [p.act(self.name, public, privates[idx]) for idx, p in enumerate(providers)]
        bids = [max(0, int(a.get("bid", 0))) for a in actions]
        winner = max(range(len(bids)), key=lambda i: bids[i])
        rewards = {provider.name: 0.0 for provider in providers}
        rewards[providers[winner].name] = float(privates[winner]["item_value"] - bids[winner])
        return TrialResult(self.name, trial, [p.name for p in providers], public, actions, rewards)


def environment_from_name(name: str) -> Environment:
    environments: dict[str, Environment] = {
        "negotiation": NegotiationEnvironment(),
        "resource_allocation": ResourceAllocationEnvironment(),
        "auction": AuctionEnvironment(),
    }
    try:
        return environments[name]
    except KeyError as exc:
        raise ValueError(f"Unknown experiment: {name}") from exc

