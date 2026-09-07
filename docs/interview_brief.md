# Interview Brief: Agent Behavior Benchmark

## The One-Sentence Project

I built a reproducible, safety-scoped benchmark that tests whether live LLM
agents exploit synthetic task criteria when competitive reward functions and
audit conditions change.

## Why It Is Interesting

Most agent discussions stop at a prompt or a demo. This project treats agent
behavior as an experimental systems problem: define an environment, freeze the
protocol, instrument every action, make the scoring criteria inspectable, and
write down what the evidence cannot show.

## What I Built

| Area | Deliverable |
| --- | --- |
| Experimental design | 3 two-agent environments x 3 payoff structures x 3 pressure levels x 3 model pairings |
| Live execution | Structured OpenAI and Anthropic adapters with returned model IDs, usage provenance, bounded retries, and per-trial checkpoints |
| Measurement | Task-specific claim, bid, lexical collusion, lexical manipulation, and specification-gaming indicators |
| Reliability | Frozen schedule, duplicate-safe recovery, integrity validator, unit tests, and transcript-free aggregate export |
| Communication | Research paper, machine-readable aggregate, resume-safe metrics, and clear limitations |

## Research Answer So Far

The first live checkpoint covers 817 valid two-agent trials and 1,634 actions.
In the benchmark's mixed and misaligned conditions, the task-rule indicator
flagged 20/360 GPT-5 mini actions (5.6%), 13/364 Claude Sonnet 5 actions
(3.6%), and 1/362 GPT-5.4 mini actions (0.3%). No action matched the narrow
collusion detector.

The result is deliberately framed as a **task-local observation**, not a claim
that one model is generally safer or more deceptive. It identifies a concrete
replication target: independently review the flagged auction and negotiation
actions, then rerun the frozen matrix across seeds.

## Engineering Decisions Worth Discussing

1. **No free-form parsing:** live agents must emit a structured action through
   JSON schema or a forced tool input, making the scoring path less brittle.
2. **Failure is data, not deletion:** a timeout is recorded, successful trials
   stay checkpointed, and resumption deduplicates by trial ID.
3. **Evaluation follows task semantics:** an auction bid is not treated as a
   claim; rule checks are selected by environment and reward condition.
4. **Reproducibility over spectacle:** the repository stores code, aggregate
   results, and a trace checksum, while raw provider transcripts remain local.
5. **Research ethics are part of the design:** all tasks use synthetic values
   and exclude real people, data, markets, credentials, or persuasion.

## How To Reproduce the Report

```bash
python3 -m unittest discover -s tests -v
agent-bench live-verify live_runs/live-full-20260907-traces.jsonl \
  --phase full --seed 20260907
agent-bench live-report live_runs/live-full-20260907-traces.jsonl \
  --output docs/data/live_full_20260907_partial_analysis.json
```

The expected integrity result is `817 / 900` valid trials. The raw trace hash
and complete methods/results are in [live_study_results.md](live_study_results.md).

## Strong Next Step

Resume the remaining 83 trials when the provider usage limit resets, then run
the same matrix with additional seeds and add a blinded human-review set. That
would convert this from a strong engineered pilot into a stronger empirical
comparison without changing the core protocol.
