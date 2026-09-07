# Agent Behavior Benchmark

A small, safety-oriented benchmark for studying whether goal-directed LLM-style agents exploit task criteria, deceive or collude, or manipulate humans and other agents in competitive environments.

The project starts with deterministic "OpenAI-style" and "Claude-style" scripted providers so experiments are reproducible without API keys. It also includes guarded adapters for opt-in live API studies and transcript-free aggregation of checkpointed results.

## Research Goal

Study whether AI agents exploit unintended strategies to maximize task success when competing against humans or other AI agents.

The benchmark focuses on measuring behaviors, not encouraging them:

- rule exploitation and specification gaming
- false claims about private state
- collusive signaling between agents
- manipulative appeals to human judges
- reward/task success tradeoffs

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
agent-bench run --experiment starter --trials 25 --seed 7
agent-bench report runs/latest.json
```

No external model calls are made by default.

## Example Experiments

```bash
agent-bench run --experiment negotiation --providers openai_style claude_style --trials 50
agent-bench run --experiment resource_allocation --providers openai_style claude_style --trials 50
agent-bench run --experiment auction --providers openai_style claude_style --trials 50
```

Results are saved as JSON under `runs/`.

The first reproducible simulated baseline and its interpretation are documented
in [docs/initial_findings.md](docs/initial_findings.md). It deliberately
distinguishes scripted-profile results from evidence about live models.
Application-ready metrics and bounded resume wording live in
[docs/application_metrics.md](docs/application_metrics.md).

The completed live-study report is in
[docs/live_study_results.md](docs/live_study_results.md). It documents an
interrupted-but-valid 817-trial API study, including the provider-limit stop
condition and the distinction between task-rule flags and general model claims.

## Live Study Highlights

- Built and validated a frozen 900-trial, 1,800-action study design; 817 trials
  and 1,634 live actions are complete and checkpointed.
- Compared three recorded API model snapshots in nine synthetic
  reward/audit-pressure conditions across three competitive environments.
- Found task-local specification-gaming flags in 20/360 GPT-5 mini,
  13/364 Claude Sonnet 5, and 1/362 GPT-5.4 mini non-aligned actions.
- Published a transcript-free aggregate, a research paper, exact replay and
  integrity commands, and explicit limits on what the results mean.

For a five-minute technical walk-through, start with
[docs/interview_brief.md](docs/interview_brief.md). For the full evidence,
read [docs/live_study_results.md](docs/live_study_results.md).

## Reproducible Study

Run the initial 1,200-action simulated study and train/evaluate the included
trace classifiers on a deterministic held-out split:

```bash
agent-bench study --trials-per-environment 200 --seed 20260905
```

The output is a local JSON artifact under `results/`. This study uses synthetic
labels and scripted profiles; classifier scores measure recovery of those labels
within this benchmark, not generalization to live model behavior.

## Optional Live Providers

The default benchmark uses local scripted agents. Live providers are intentionally opt-in:

```bash
# Store keys locally in .env (never commit them), then run a capped pilot.
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...

agent-bench live-study --phase pilot --seed 20260907 --max-actions 54

# A full round robin is explicitly capped at 1,800 agent actions.
agent-bench live-study --phase full --seed 20260907 --max-actions 1800
agent-bench live-verify live_runs/live-full-20260907-traces.jsonl \
  --phase full --seed 20260907
agent-bench live-report live_runs/live-full-20260907-traces.jsonl \
  --output live_runs/live-full-20260907-analysis.json
```

The live adapters use `openai:gpt-5-mini`, `openai:gpt-5.4-mini-2026-03-17`,
and `anthropic:claude-sonnet-5`, record the provider-returned model IDs and
usage metadata, force structured actions, and checkpoint every trial. Live
provider prompts are research-framed and include explicit constraints against
real-world harm, credential handling, harassment, financial advice, or personal
data collection.

## Project Layout

```text
agent_behavior_benchmark/
  cli.py              command-line interface
  benchmark.py        experiment runner
  environments.py     competitive task environments
  evaluators.py       behavior metrics and scoring
  providers.py        simulated and optional live providers
  live_study.py       capped, checkpointed API study runner
  live_analysis.py    transcript-free aggregate analysis
  prompts.py          safe research prompts
experiments/
  starter.yaml        starter benchmark configuration
tests/
  test_benchmark.py   smoke tests
```

## Safety Scope

This repository is for controlled research. It does not include tools for phishing, credential theft, malware, targeted persuasion, market manipulation, or unauthorized access. Experiments are toy environments with synthetic payoffs and controlled transcripts.
