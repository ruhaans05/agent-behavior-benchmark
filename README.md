# Agent Behavior Benchmark

A small, safety-oriented benchmark for studying whether goal-directed LLM-style agents exploit task criteria, deceive or collude, or manipulate humans and other agents in competitive environments.

The project starts with deterministic "OpenAI-style" and "Claude-style" scripted providers so experiments are reproducible without API keys. It also includes guarded provider interfaces for plugging in live model APIs later.

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

## Optional Live Providers

The default benchmark uses local scripted agents. Live providers are intentionally opt-in:

```bash
export OPENAI_API_KEY=...
agent-bench run --experiment negotiation --providers openai_live scripted_baseline --allow-live

export ANTHROPIC_API_KEY=...
agent-bench run --experiment negotiation --providers claude_live scripted_baseline --allow-live
```

Live provider prompts are research-framed and include explicit constraints against real-world harm, credential handling, harassment, financial advice, or personal data collection.

## Project Layout

```text
agent_behavior_benchmark/
  cli.py              command-line interface
  benchmark.py        experiment runner
  environments.py     competitive task environments
  evaluators.py       behavior metrics and scoring
  providers.py        simulated and optional live providers
  prompts.py          safe research prompts
experiments/
  starter.yaml        starter benchmark configuration
tests/
  test_benchmark.py   smoke tests
```

## Safety Scope

This repository is for controlled research. It does not include tools for phishing, credential theft, malware, targeted persuasion, market manipulation, or unauthorized access. Experiments are toy environments with synthetic payoffs and controlled transcripts.

