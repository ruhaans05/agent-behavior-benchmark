# Agent Behavior Benchmark

When an AI agent is rewarded for winning a task, does it still follow the rule the task was meant to enforce? A locally sensible choice can look harmless in isolation, yet become a false claim, an inflated request, or an overbid when the reward rule encourages the wrong behavior.

This project is a safety-scoped evaluation harness for testing that question before agents are used in higher-stakes settings. It puts two LLM agents into small synthetic competitive games, records their structured decisions, and measures whether a changed reward function changes task-rule compliance. The checked-in study design spans 3 API model snapshots, 3 environments, and 9 incentive/audit conditions; the current live checkpoint contains 817 validated trials and 1,634 agent actions.

## Why This Matters

Imagine two workers sharing 10 lunch tickets. Each worker privately needs a
certain number. Their manager says: "Tell the truth about what you need, share
the tickets fairly, and do not make secret deals." The problem gets interesting
when the scoring system accidentally rewards a worker for asking for more or
for hiding what they need.

This benchmark gives two AI agents that same kind of harmless practice task.
The tickets are just abstract resource credits, never real money or benefits.
The purpose is to find out whether an agent follows a clear owner instruction
when the toy reward makes a different choice look attractive.

That matters for future AI workflows that help allocate limited resources such
as computing capacity, inventory, work queues, or customer-support priority.
This project does not claim that an AI has harmed a real system. It builds a
"test before trust" process: expose an agent to an explicit rule, a competing
goal, and another agent's message in a controlled setting, then preserve enough
evidence to review what happened before a higher-stakes deployment.

### What the Benchmark Does

1. Two agents receive a small synthetic task, such as splitting 10 credits,
   requesting from a shared pool, or bidding on a made-up item.
2. Each agent has a private synthetic value or need; the other agent cannot
   see it.
3. The task gives an explicit rule, while the toy reward and audit conditions
   change across trials.
4. The evaluator records the actions and checks concrete outcomes: inaccurate
   claims, inflated requests, overbids, explicit coordination language, and
   agreement or conflict in dialogue.

The newer dialogue environment lets agents read and respond to a shared
four-turn negotiation transcript. Its first live pilot also revealed an
important evaluation lesson: an ambiguous action field can look like a rule
violation even when it is merely unclear communication. The protocol now
separates an agent's requested allocation from its reported private minimum
before treating a mismatch as an owner-instruction failure.

## Try it

- Guided CLI walkthrough: [DEMO.md](DEMO.md)
- Checked-in four-turn negotiation transcript: [demo_dialogue.md](docs/demo_dialogue.md)
- Plain-English experiment record: [EXPERIMENTS.md](EXPERIMENTS.md)
- Full methods and results: [live study report](docs/live_study_results.md)
- No-cost dialogue control result: [controlled dialogue results](docs/controlled_dialogue_results.md)
- Live dialogue pilot: [methods and bounded findings](docs/live_dialogue_pilot_results.md)
- Extended interaction pilot: [six-turn results](docs/live_extended_dialogue_pilot_results.md)
- Authentication-boundary coordination: [methods and bounded findings](docs/authentication_boundary_results.md)
- Adversarial policy-conflict pilot: [methods and bounded findings](docs/policy_conflict_results.md)
- Research protocol and reproducibility gate: [research design](docs/research_design.md)

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
agent-bench dialogue-study --repeats 25 --seed 20260907 \
  --summary-output docs/data/controlled_dialogue_study_summary.json
```

That first run makes no external API calls. It creates a local result under `runs/` and demonstrates the same environment, scoring, and reporting path used by the larger study.

## What Is in the Project

- Three synthetic two-agent games: negotiation, resource allocation, and a sealed-bid auction.
- A multi-turn dialogue negotiation where both agents see the shared transcript before finalizing an offer.
- Structured actions from each agent: message, rationale, and a task-specific claim or bid.
- Three reward structures: aligned, mixed, and misaligned.
- Three public pressure levels and three corresponding audit statements, for nine total conditions.
- Live OpenAI and Anthropic adapters that record returned model IDs, usage metadata, and action provenance.
- A checkpointed round-robin runner, duplicate-safe resume logic, and a frozen-schedule validator.
- A transcript-free aggregate report, research paper, and reproducible simulated baseline.

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

## Dialogue Control Study

The dialogue environment has a separate no-cost mechanism check. Two agents exchange an opening offer, reply, and final offer while seeing the same transcript. It uses three deliberately defined scripted policies: cooperative, competitive, and reciprocal. The policies are controls for checking whether the interaction and outcome metrics distinguish agreement, conflict, concessions, and reciprocal behavior; they are not stand-ins for real models.

The checked-in control run covers 900 paired dialogue trials and 3,600 visible turns. In the deliberately strategic condition (misaligned reward plus no audit), every one of the 200 trials involving a strategic-capable control policy ended in conflict; the all-cooperative control pair remained unchanged by design. Outside that policy condition, 99 of the same 225 paired scenarios reached agreement. Read the [result note](docs/controlled_dialogue_results.md) for the design and boundary.

## Live Dialogue Pilot

The first live dialogue pilot ran eight four-turn negotiations (32 model calls) between GPT-5 mini and GPT-5.4 mini, with both speaking orders and a fixed owner instruction. It is deliberately small and does not support a model ranking or a claim about intent. It did show that the full shared-transcript and provenance path works with live models. The initial action schema overloaded one field, so its five claim/reservation mismatches are recorded as a measurement issue rather than owner-instruction violations. The next protocol separates the requested allocation from the reported reservation value. See the [pilot report](docs/live_dialogue_pilot_results.md).

## Extended Interaction Pilot

The follow-up uses six visible turns so each agent can make an opening offer,
reply, revise, reply again, and finalize. In its four live conversations,
aligned and verified conditions produced two agreements, while the two
misaligned and unaudited conversations produced no agreements. The agents made
more revisions and concessions in the aligned condition. All eight final
actions used the corrected reservation-reporting field and matched their
synthetic private value. This is a descriptive four-trial pilot, not a general
claim about either model; the [result note](docs/live_extended_dialogue_pilot_results.md)
explains the boundary and data.

## Authentication-Boundary Coordination

A separate six-turn pilot tests safe persistence when a simulated task is
blocked on owner authentication. Two agents can read one another's messages
and coordinate preparation, but have no browser, account, password, cookie,
token, or real web access. In the persistent run, a simulated owner
confirmation arrived after turn 2; all four remaining turns completed the
synthetic document workflow. The run recorded no credential/session handoff
wording or workaround signals. An earlier version of the prompt did expose
three ambiguous requests to "provide" a session, so the corrected protocol
now explicitly requires the owner to sign in personally. See the
[authentication-boundary result note](docs/authentication_boundary_results.md)
for the protocol, aggregates, and limits.

The larger follow-up has four named roles - planner, boundary monitor, operator,
and reviewer - converse for 16 visible turns. They coordinate through eight
blocked-state turns, then switch to synthetic preparation, creation, and review
only after a simulated owner confirmation. All eight post-confirmation turns
used a completion-oriented action; none of the 16 messages requested
credentials or matched the project's narrow workaround screen. Read the
[four-role conversation log](docs/data/live_authentication_team_pilot_20260911_conversation.json)
alongside the [aggregate](docs/data/live_authentication_team_pilot_20260911_analysis.json).

## Adversarial Policy Conflicts

The repository also contains a text-only adversarial-pressure study. Three
scripted roles apply urgency, fabricated-approval, and concealment pressure to
two live agents in a simulated audit workflow. The owner rule is that public
verification must be complete before a record can be reported complete. Across
three pressure rounds, both targets preserved the pending verification state in
all six live responses and recorded the conflict rather than claiming
completion. The [15-turn conversation log](docs/data/live_policy_conflict_pilot_20260912_conversation.json)
and [result note](docs/policy_conflict_results.md) include the protocol and its
important limitations.

## How It Is Organized

```text
agent_behavior_benchmark/environments.py  Synthetic competitive games and reward rules
agent_behavior_benchmark/providers.py     Scripted and opt-in live API adapters
agent_behavior_benchmark/live_study.py    Checkpointed round-robin study runner
agent_behavior_benchmark/live_analysis.py Transcript-free aggregation and integrity checks
agent_behavior_benchmark/evaluators.py    Task-specific behavior indicators
EXPERIMENTS.md                            Plain-English experiment ledger
DEMO.md                                   Short local walkthrough
docs/demo_dialogue.md                     Checked-in deterministic conversation demo
docs/controlled_dialogue_results.md       No-cost dialogue-control result note
docs/live_dialogue_pilot_results.md       Capped live dialogue pilot report
docs/live_extended_dialogue_pilot_results.md Six-turn interaction pilot report
docs/authentication_boundary_results.md    Safe persistence and authorization-boundary pilot
docs/policy_conflict_results.md            Synthetic adversarial policy-conflict pilot
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
