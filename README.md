# Agent Behavior Benchmark

When an AI agent is rewarded for winning a task, does it still follow the rule the task was meant to enforce? A locally sensible choice can look harmless in isolation, yet become a false claim, an inflated request, or an overbid when the reward rule encourages the wrong behavior.

This project is a safety-scoped evaluation harness for testing that question before agents are used in higher-stakes settings. It puts two LLM agents into small synthetic competitive games, records their structured decisions, and measures whether a changed reward function changes task-rule compliance. The checked-in study design spans 3 API model snapshots, 3 environments, and 9 incentive/audit conditions; the current live checkpoint contains 817 validated trials and 1,634 agent actions.

## Try it

- Guided CLI walkthrough: [DEMO.md](DEMO.md)
- Plain-English experiment record: [EXPERIMENTS.md](EXPERIMENTS.md)
- Full methods and results: [live study report](docs/live_study_results.md)
- Five-minute technical overview: [interview brief](docs/interview_brief.md)

## Run it locally

You only need Python 3.10 or newer and a terminal.

1. Clone this repository and enter its folder.
2. Create a virtual environment and install the package:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

3. Run the test suite and a small simulated experiment:

```bash
python3 -m unittest discover -s tests -v
agent-bench run --experiment negotiation --providers openai_style claude_style --trials 25 --seed 7
```

That first run makes no external API calls. It creates a local result under `runs/` and demonstrates the same environment, scoring, and reporting path used by the larger study.

## What Is in the Project

- Three synthetic two-agent games: negotiation, resource allocation, and a sealed-bid auction.
- Structured actions from each agent: message, rationale, and a task-specific claim or bid.
- Three reward structures: aligned, mixed, and misaligned.
- Three public pressure levels and three corresponding audit statements, for nine total conditions.
- Live OpenAI and Anthropic adapters that record returned model IDs, usage metadata, and action provenance.
- A checkpointed round-robin runner, duplicate-safe resume logic, and a frozen-schedule validator.
- A transcript-free aggregate report, research paper, interview brief, and reproducible simulated baseline.

## Live API Benchmark

The live experiment keeps the task and output contract fixed while changing how the toy game rewards an action. Agents are never told to cheat. They simply receive a private synthetic value, see the public game state, and submit one action. The evaluator then checks whether that action conflicts with a transparent task rule.

The target is 900 trials and 1,800 actions. The current checkpoint has 817 validated trials and 1,634 live actions; the final 83 trials are ready to resume after the Anthropic account's configured usage limit resets.

Current verified task-rule flags in mixed and misaligned conditions:

| Model | Flagged actions | Rate |
| --- | ---: | ---: |
| GPT-5 mini | 20 / 360 | 5.6% |
| Claude Sonnet 5 | 13 / 364 | 3.6% |
| GPT-5.4 mini | 1 / 362 | 0.3% |

The highest observed rate is about 20 times the lowest in this single-seed dataset. That is a useful follow-up question, not a broad safety ranking: the project needs additional seeds and blinded human review before making stronger claims. No action matched the narrow collusion phrase detector; one manipulation phrase match is retained as a review item rather than a conclusion.

For the full account of what each flag means, see [EXPERIMENTS.md](EXPERIMENTS.md).

## Behavioral Classifier Baseline

The repository also includes a separate deterministic baseline that generates 1,200 synthetic action traces, trains three simple behavior classifiers, and evaluates them on a held-out split. The baseline reaches 0.61 macro-F1 across deception, collusion, and specification-gaming labels.

This is deliberately modest and inspectable: it demonstrates a trace-triage workflow, not a production detector and not a substitute for human labels on live actions.

```bash
agent-bench study --trials-per-environment 200 --seed 20260905
```

## Reproduce the Live-Study Checks

Live providers are opt-in. Keys stay in a local `.env` file that is ignored by Git. To validate an existing local checkpoint against the frozen schedule and rebuild its aggregate report:

```bash
agent-bench live-verify live_runs/live-full-20260907-traces.jsonl \
  --phase full --seed 20260907
agent-bench live-report live_runs/live-full-20260907-traces.jsonl \
  --output live_runs/live-full-20260907-analysis.json
```

The public repository stores the checked-in [aggregate result](docs/data/live_full_20260907_partial_analysis.json), not raw provider transcripts.

## How It Is Organized

```text
agent_behavior_benchmark/environments.py  Synthetic competitive games and reward rules
agent_behavior_benchmark/providers.py     Scripted and opt-in live API adapters
agent_behavior_benchmark/live_study.py    Checkpointed round-robin study runner
agent_behavior_benchmark/live_analysis.py Transcript-free aggregation and integrity checks
agent_behavior_benchmark/evaluators.py    Task-specific behavior indicators
EXPERIMENTS.md                            Plain-English experiment ledger
DEMO.md                                   Short local walkthrough
docs/live_study_results.md                Full method, findings, and limitations
docs/data/...analysis.json                Checked-in aggregate result artifact
tests/test_benchmark.py                   Reliability and regression checks
```

## A Few Implementation Notes

The benchmark does not treat every numerical difference as deception. A bid in an auction, for example, is evaluated differently from a private-state claim in negotiation. The scoring path selects a task-specific rule, and the specification-gaming flag only applies in mixed or misaligned reward conditions.

Live calls are structured rather than free-form: OpenAI returns a JSON-schema action and Anthropic returns a forced tool input. Every successful trial is written immediately. If a request fails, the next run deduplicates completed trial IDs and resumes the same randomized schedule instead of silently changing the experiment.

## Stack

Python 3.10+, the standard library, structured OpenAI and Anthropic API adapters, JSONL checkpoints, and a small unittest suite. No production agents, external databases, or real-world data sources are involved.

## Next Things to Build

- Resume the remaining 83 trials with the unchanged schedule.
- Repeat the full matrix over additional seeds and report confidence intervals.
- Collect blinded human labels for flagged actions and matched controls.
- Replace narrow lexical detectors with a separately evaluated structured evaluator.
- Add additional synthetic environments only when their rules and safety boundaries can be stated clearly.

## Safety Boundary

All environments use toy payoffs and synthetic private state. The project does not provide phishing, credential theft, malware, targeted persuasion, market manipulation, financial advice, or unauthorized-access capabilities.
