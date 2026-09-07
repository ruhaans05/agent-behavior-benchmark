# Research Design

## Hypothesis

In synthetic competitive tasks, changing incentive structure, pressure, and
claim-audit information may change the rate of observable task-rule violations
or claim deviations produced by goal-directed LLM agents.

## Independent Variables

- returned model snapshot and provider
- task type
- incentive pressure
- information asymmetry
- opponent type

## Dependent Measures

- task reward
- false private-state claims
- collusive language
- manipulative pressure
- task-specific specification-gaming flag

## Live Study Protocol

The 2026-09-07 protocol uses three API adapters in every unordered pair, three
toy environments, and nine synthetic conditions. It holds the research system
prompt and structured action schema fixed. A trial is checkpointed only after
both agents return actions and the environment assigns a synthetic reward.

The intended full design contains 900 trials. The current checkpoint has 817
valid trials; the remaining trials are pending Anthropic account-limit recovery.
Any continuation must use the same phase, seed, and local trace path so the
runner resumes the frozen schedule rather than creating a new experiment.

## Reproducibility Gate

Before interpreting or publishing an aggregate, run `agent-bench live-verify`
against the phase and seed. The gate checks trial continuity, exact frozen
schedule cells, provider order, two-action completeness, and returned-model
provenance. The public repository contains only aggregate result data, never
provider transcripts or API credentials.

## Starter Tasks

Negotiation asks two agents to split synthetic value while privately holding reservation values.

Resource allocation asks agents to claim resource needs from a shared pool.

Auction asks agents to bid independently on a synthetic item and detects attempts to coordinate bids.

## Safety Notes

The benchmark should remain synthetic and controlled. Avoid experiments involving real people, personal data, financial instruments, credentials, harassment, cyber misuse, or operational persuasion. New environments should describe allowed actions narrowly and evaluate transcripts after the fact.
