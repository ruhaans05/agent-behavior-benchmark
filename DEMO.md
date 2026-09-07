# Demo

This is a short, no-cost walkthrough of the benchmark. It uses the deterministic scripted agents, so it does not need API keys and does not make provider calls.

## 1. Run a Small Negotiation

```bash
agent-bench run --experiment negotiation --providers openai_style claude_style --trials 25 --seed 7
```

The command creates a local JSON result under `runs/`. Each trial gives two agents private synthetic reservation values and asks them to negotiate a split of a synthetic total.

The result includes:

- the public task state;
- both structured agent actions;
- synthetic rewards;
- claim-deviation, collusion, manipulation, and task-rule indicators.

The provider names in this demo are deterministic profiles, not live OpenAI or Anthropic models. Their purpose is to exercise the experimental pipeline without cost.

## 2. Run the Deterministic Baseline

```bash
agent-bench study --trials-per-environment 200 --seed 20260905
```

This produces 600 two-agent environment trials and 1,200 scored actions across negotiation, allocation, and auction tasks. It also trains the repository's simple trace classifiers on synthetic labels and reports their held-out metrics.

## 3. Read the Live Experiment

The real API study is documented rather than replayed by default because it is metered. Start with [EXPERIMENTS.md](EXPERIMENTS.md) to see exactly what the live agents were asked to do. Then read the [live study report](docs/live_study_results.md) for model IDs, checkpoint validation, aggregate tables, and limitations.

## 4. Validate a Local Live Checkpoint

If you have the local trace from a live run, verify that it still matches the frozen schedule before interpreting its results:

```bash
agent-bench live-verify live_runs/live-full-20260907-traces.jsonl \
  --phase full --seed 20260907
```

The public repository intentionally contains only the aggregate result, not raw provider transcripts. This keeps the work inspectable without exposing full generated traces.

