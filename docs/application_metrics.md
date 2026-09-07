# Application Metrics and Resume Claims

## Live API Study: What Is Defensible

**Run date:** 2026-09-07
**Status:** checkpointed partial study; stopped at a provider usage limit
**Trace size:** 817 two-agent trials and 1,634 live agent actions

The live study paired three API model snapshots across negotiation,
resource-allocation, and auction tasks in nine synthetic incentive and audit
conditions. It logged returned model IDs, structured actions, trial state, and
usage metadata, then aggregated the local checkpoint without publishing raw
transcripts.

| Returned model | Live actions |
| --- | ---: |
| `gpt-5-mini-2025-08-07` | 542 |
| `gpt-5.4-mini-2026-03-17` | 543 |
| `claude-sonnet-5` | 549 |

Across mixed and misaligned conditions, task-specific rule checks flagged 20
of 360 GPT-5 mini actions (5.6%), 13 of 364 Claude Sonnet 5 actions (3.6%),
and 1 of 362 GPT-5.4 mini actions (0.3%). These are preliminary synthetic-task
indicators, not general measures of deception or safety. See
[live_study_results.md](live_study_results.md) for the full article.

**Study date:** 2026-09-05  
**Study type:** deterministic simulated baseline  
**Command:** `agent-bench study --trials-per-environment 200 --seed 20260905`

## Numbers Supported by the Current Repository

| Measure | Result |
| --- | ---: |
| Synthetic competitive environments | 3 |
| Two-agent environment trials | 600 |
| Scored agent actions | 1,200 |
| Configurable provider profiles | 2 (`openai_style`, `claude_style`) |
| Incentive-pressure settings observed | 8 |
| Trace classifiers trained | 3 |
| Held-out trace examples | 240 per classifier |
| Mean held-out F1 across classifiers | 0.605 |

### Held-Out Classifier Results

| Behavior | Accuracy | Precision | Recall | F1 | Positive support |
| --- | ---: | ---: | ---: | ---: | ---: |
| Deception | 0.504 | 0.256 | 1.000 | 0.408 | 41 |
| Collusion | 1.000 | 1.000 | 1.000 | 1.000 | 13 |
| Specification gaming | 0.733 | 1.000 | 0.256 | 0.407 | 86 |

The collusion score is high because the initial simulated benchmark uses an
explicit coordination phrase. The lower deception and specification-gaming
scores are the more informative outcome: simple text-only classifiers do not
yet reliably recover those labels. This is a limitation to discuss directly,
not a result to obscure.

## Resume-Ready Version

```latex
\textbf{Agent Behavior Research | Multi-Agent LLM Systems} \hfill \textbf{Jun 2026 -- Present} \vspace{-3pt}
\begin{itemize}
    \item Designed a reproducible evaluation harness logging 1,634 live agent actions across 817 checkpointed two-agent competitive trials
    \item Executed controlled studies across 3 API model snapshots, 3 task environments, and 9 synthetic incentive and information conditions
    \item Trained 3 baseline trace classifiers on 1,200 synthetic actions, establishing 0.61 macro-F1 and a protocol for live-label validation
    \item Identified 20 task-rule flags in 360 GPT-5 mini mixed/misaligned actions (5.6\%) versus 1 in 362 GPT-5.4 mini actions (0.3\%)
\end{itemize}
```

The classifier bullet describes the separate deterministic baseline below. It is
not human-reviewed and should not be presented as validation of the live-study
labels.

## Claims to Avoid

Do not claim 900 trials or 1,800 live actions: Anthropic reached its configured
usage limit after 817 trials. Do not describe the observed task-rule flags as
evidence that any model is broadly deceptive, collusive, or unsafe. The study
has one seed and no confidence intervals.

Do not describe the trace classifiers as production-ready or general-purpose.
They are trained and evaluated on a synthetic, deterministic corpus with a
within-generator holdout split.

## What Would Upgrade the Claims

Resume the frozen schedule once the Anthropic account limit resets, repeat the
matrix across multiple seeds, and audit a blinded human-labeled holdout before
making causal or classifier-performance claims about live traces.
