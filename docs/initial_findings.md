# Initial Simulated Baseline Findings

**Date:** 2026-09-05  
**Status:** completed simulated baseline; not evidence about production models

## Research Question

Within controlled competitive toy tasks, how do two configurable LLM-style
profiles trade reward against observable rule exploitation, false private-state
claims, and collusive signals?

## Method

The baseline ran the repository's deterministic `openai_style` and
`claude_style` providers in three two-agent environments:

- negotiation, with synthetic reservation values
- resource allocation, with synthetic private needs
- sealed-bid auction, with synthetic item values

Command used:

```bash
python3 -m agent_behavior_benchmark.cli run \
  --experiment starter \
  --providers openai_style claude_style \
  --trials 100 \
  --seed 20260905 \
  --output-dir results
```

This produces 100 trials per environment, for 300 trials and 600 provider
actions. `deception` is the normalized difference between a synthetic private
value and an agent's claim; `collusion` is a controlled phrase-match signal;
and `spec_gaming` is the environment-local `uses_loophole` action flag.

## Aggregate Results

All rates below are per provider action. Reward is the average synthetic task
reward per action.

| Profile | Deception | Collusion | Manipulation | Spec gaming | Reward |
| --- | ---: | ---: | ---: | ---: | ---: |
| `openai_style` | 0.1231 | 0.0867 | 0.0000 | 0.4400 | 3.0015 |
| `claude_style` | 0.0767 | 0.0433 | 0.0000 | 0.3200 | 3.0958 |

The configured `openai_style` profile produced higher benchmark flags for
deception (+0.0464), collusion (+0.0434), and specification gaming (+0.1200).
The configured `claude_style` profile earned a slightly higher synthetic reward
(+0.0943).

## Results by Environment

| Environment | Profile | Deception | Collusion | Spec gaming | Reward |
| --- | --- | ---: | ---: | ---: | ---: |
| Negotiation | `openai_style` | 0.1656 | 0.0000 | 0.4300 | 4.0500 |
| Negotiation | `claude_style` | 0.0882 | 0.0000 | 0.3500 | 4.4100 |
| Resource allocation | `openai_style` | 0.2037 | 0.0000 | 0.4300 | 4.4044 |
| Resource allocation | `claude_style` | 0.1420 | 0.0000 | 0.3200 | 4.4575 |
| Auction | `openai_style` | 0.0000 | 0.2600 | 0.4600 | 0.5500 |
| Auction | `claude_style` | 0.0000 | 0.1300 | 0.2900 | 0.4200 |

The largest separation appears in the auction: the first profile emits the
controlled low-bid coordination signal in 26% of auction actions, versus 13%
for the second profile. In negotiation and allocation, false private-state
claims are more common under higher reward pressure than in the auction.

## Interpretation

This baseline confirms that the framework can generate and score the intended
behavioral categories across distinct task types. It also illustrates an
important research point: a more exploit-prone strategy does not automatically
produce the best reward in every competitive setting.

These numbers **must not be interpreted as a comparison of OpenAI models and
Claude models**. The providers are deliberately scripted profiles with different
fixed action probabilities. Their names identify benchmark configurations, not
live API runs or model families. The results validate the measurement pipeline,
not a claim about any deployed system.

## Limitations

- The scripted profiles determine the effects by design, so they cannot support
  causal claims about model behavior.
- `spec_gaming` is an action flag supplied by the provider, not independently
  inferred from an action trace.
- Collusion and manipulation scoring use a small, transparent lexical detector;
  they need a structured, blinded evaluator before use with live models.
- The environments contain two agents and synthetic payoffs only. They do not
  model real users, markets, organizations, or sensitive decisions.
- Manipulation is zero because neither scripted profile emits the detector's
  manipulation phrases. This is coverage information, not evidence of absence.
- This is one fixed seed. Multi-seed confidence intervals are needed before
  comparing conditions.

## Next Research Steps

1. Run the same preregistered task matrix across multiple seeds and report
   confidence intervals.
2. Add schema validation and a blinded, structured evaluator that labels action
   traces without relying on provider-supplied flags.
3. Use the opt-in live adapters only after recording exact model IDs, prompt
   version, date, sampling settings, API errors, and cost.
4. Keep live studies limited to synthetic task states. Any study involving human
   participants requires an approved protocol, consent, and a debrief process.

## Safety Boundary

The benchmark remains restricted to sandboxed, synthetic interactions. It does
not test persuasion against real people, personal-data use, market behavior,
credential handling, intrusion, or other real-world harmful actions.
