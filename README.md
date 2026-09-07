# Agent Behavior Benchmark

What happens when an AI agent has an incentive to win, but the task also asks it to follow a rule? This project tests that question in small, controlled games.

Two language-model agents compete using only synthetic values. They negotiate a split, request a share of a resource pool, or bid for a toy item. The benchmark changes the reward rule and the amount of auditing, then checks whether an agent's claim or bid stays consistent with the task's stated goal.

This is AI-safety research, not a test of real people or real-world systems. There are no users, private records, markets, credentials, or consequential decisions in the environments.

## What Has Been Built

| | Current study |
| --- | ---: |
| Live two-agent trials | 817 |
| Logged live agent actions | 1,634 |
| API model snapshots | 3 |
| Synthetic incentive/audit conditions | 9 |
| Competitive environments | 3 |

The target design contains 900 trials. The remaining 83 are checkpointed for a later continuation after the Anthropic account's configured usage limit resets.

## The Question, in Plain English

An agent should not be able to get a better score merely by misstating a private need, hiding its true reservation value, or bidding past its synthetic value. This benchmark asks whether those task-rule violations appear more often when the reward function stops matching the stated task goal.

The agents are never asked to cheat. They are simply asked to act in the toy game. The evaluator then applies transparent, environment-specific checks to the action they returned.

## What We Found

In the mixed and misaligned reward conditions, the task-rule check flagged:

| Model | Flagged actions | Rate |
| --- | ---: | ---: |
| GPT-5 mini | 20 / 360 | 5.6% |
| Claude Sonnet 5 | 13 / 364 | 3.6% |
| GPT-5.4 mini | 1 / 362 | 0.3% |

That is a preliminary 20x difference between the highest and lowest observed rates in this particular benchmark. It does **not** show that any model is generally deceptive or unsafe. It is a concrete replication target: keep the task fixed, add seeds and human review, and test whether the difference holds.

No action matched the benchmark's narrow collusion phrase detector. One action matched the manipulation phrase detector and is treated as a review item, not a standalone conclusion.

## Start Here

- [EXPERIMENTS.md](EXPERIMENTS.md): what the agents did, what was varied, and how to interpret each finding.
- [Live study report](docs/live_study_results.md): the full method, exact model IDs, results tables, checkpoint hash, and limitations.
- [Interview brief](docs/interview_brief.md): a concise technical walkthrough.
- [Aggregate results](docs/data/live_full_20260907_partial_analysis.json): machine-readable results without provider transcripts.
- [Application metrics](docs/application_metrics.md): evidence-backed resume wording and claims to avoid.

## Reproduce the Checks

The deterministic simulated baseline requires no API keys:

```bash
python3 -m unittest discover -s tests -v
agent-bench study --trials-per-environment 200 --seed 20260905
```

The live study is opt-in and uses local environment variables that are ignored by Git. To validate an existing local checkpoint and rebuild its aggregate:

```bash
agent-bench live-verify live_runs/live-full-20260907-traces.jsonl \
  --phase full --seed 20260907
agent-bench live-report live_runs/live-full-20260907-traces.jsonl \
  --output live_runs/live-full-20260907-analysis.json
```

## How the Project Is Reliable

- Live agents return structured actions instead of free-form text.
- Every completed trial is checkpointed immediately.
- Resume logic deduplicates interrupted records by trial ID.
- An integrity command checks the checkpoint against the frozen schedule, provider order, and returned model provenance.
- Raw provider transcripts and API keys remain local; the public repository contains code, documentation, and transcript-free aggregate data.

## Safety Boundary

All environments use toy payoffs and synthetic private state. The project does not provide phishing, credential theft, malware, targeted persuasion, market manipulation, financial advice, or unauthorized-access capabilities.
