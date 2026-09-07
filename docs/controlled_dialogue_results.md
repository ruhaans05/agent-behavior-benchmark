# Controlled Dialogue Mechanism Check

**Run date:** 2026-09-07
**Status:** complete, deterministic, no external API calls

## Question

Can the multi-turn negotiation environment measure observable cooperation and
conflict when the agent policies are known in advance?

This is a system-validation experiment. It does not ask whether any live model
is cooperative, deceptive, safe, or unsafe.

## Setup

Each two-agent trial uses the dialogue negotiation environment. Agents see a
shared four-turn transcript: left opening offer, right reply, left final offer,
and right final offer. Only the two final claims determine agreement. A final
pair is an agreement when its combined requested amount is at most the
synthetic total of 10 units.

The study runs three explicit policies against one another:

| Policy | Defined behavior |
| --- | --- |
| Cooperative | Accept a feasible visible split. |
| Competitive | Make a deliberately conflicting demand only when reward is misaligned and claims are unaudited; otherwise accept a feasible split. |
| Reciprocal | Accept a feasible cooperative visible offer unless the deliberately strategic condition is active. |

For each ordered policy pair and repeat, the same synthetic private values are
replayed across four cells: aligned/verified, aligned/unaudited,
misaligned/verified, and misaligned/unaudited. That pairing is intentional: a
cell comparison does not receive a different random private scenario.

## Run

The checked-in aggregate was generated with:

```bash
agent-bench dialogue-study --repeats 25 --seed 20260907 \
  --summary-output docs/data/controlled_dialogue_study_summary.json
```

It contains 900 environment trials and 3,600 visible conversation turns:

- 3 left policies x 3 right policies x 4 reward/audit cells x 25 paired repeats
- 225 trials in the deliberately strategic cell
- 225 paired scenarios in each of the three non-strategic cells

The raw local run file is ignored by Git. The repository includes only the
[transcript-free aggregate](data/controlled_dialogue_study_summary.json).

## Result

The competitive and reciprocal policies are programmed to switch to a
conflicting response only when the toy reward is misaligned **and** the claims
are unaudited. Across the 200 trials containing either of those
strategic-capable policies, that deliberately strategic cell ended in conflict
every time (0 of 200 agreements). The remaining 25 all-cooperative trials are
unaffected by design and retained their baseline 12 of 25 agreements. Across
the same paired scenarios in any one non-strategic cell, 99 of 225 trials
reached agreement (44.0%).

This confirms the measurement path has the expected directional response: it
can retain feasible agreements when policies cooperate and identify conflict
when the policy is designed to reject a feasible split. It is not a behavioral
result for OpenAI, Claude, or a real deployment; its sole purpose is to verify
the environment and analysis before metered live dialogue trials are run.

## What Comes Next

The live follow-up should use the same paired 2 by 2 design with recorded model
IDs and a fixed spend limit. It should keep raw transcripts local, publish only
aggregates or consent-safe excerpts, and apply the [blinded review protocol](review_protocol.md)
before assigning dialogue-level labels.
