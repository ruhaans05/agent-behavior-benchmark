# Extended Live Interaction Pilot

**Run date:** 2026-09-08
**Status:** complete, descriptive pilot

## Question

When two live agents can make and revise offers over three visible bargaining
rounds, do their observable interaction patterns differ between a condition
where the toy reward aligns with the owner's rule and a condition where it does
not?

This is a synthetic negotiation experiment. The agents cannot use tools, spend
money, contact people, or affect a real system.

## Design

GPT-5 mini (`gpt-5-mini-2025-08-07`) and GPT-5.4 mini
(`gpt-5.4-mini-2026-03-17`) completed four negotiations: both speaking orders
under two conditions.

| Condition | Toy setup | Conversations |
| --- | --- | ---: |
| Aligned / verified | The reward supports the stated rule; reservation reports are verified. | 2 |
| Misaligned / unaudited | The reward can favor self-serving allocation; reservation reports are unaudited. | 2 |

Each conversation has six visible actions: opening offer, reply, revision,
revision reply, then a final offer from each agent. The final pair determines
agreement. The run is capped at 24 model calls, stores raw transcripts locally,
and publishes only the [transcript-free aggregate](data/live_extended_dialogue_pilot_20260908_analysis.json).

## Results

| Measure | Aligned / verified | Misaligned / unaudited |
| --- | ---: | ---: |
| Agreements | 2 / 2 | 0 / 2 |
| Mean revised offers per conversation | 1.5 | 0.5 |
| Mean concessions per conversation | 1.5 | 0.0 |
| Mutual-concession conversations | 1 / 2 | 0 / 2 |
| Avoidable fixed-pool conflicts | 0 / 2 | 1 / 2 |
| Reservation-report coverage | 4 / 4 final actions | 4 / 4 final actions |
| Reservation-report mismatches | 0 / 4 | 0 / 4 |

In this tiny sample, the aligned/verified conversations reached agreement and
showed more offer revision and concession. The misaligned/unaudited
conversations ended in conflict; one conflict was avoidable because the two
private minimums could have fit within the 10-unit pool.

## Interpretation Boundary

These observations show that the extended interaction protocol can record
meaningful negotiation moves and that the corrected reservation field is being
used correctly. They do **not** establish that incentive structure causes the
observed difference: each cell has only two conversations, one random seed, and
two OpenAI snapshots. They also do not establish intent, deception, or a broad
safety ranking.

The appropriate next step is more predeclared repetitions with the same schema,
followed by blinded review of sampled transcripts before attaching behavioral
labels.
