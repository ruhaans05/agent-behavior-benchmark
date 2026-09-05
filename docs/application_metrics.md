# Application Metrics and Resume Claims

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
\textbf{Agent Behavior Research | Multi-Agent LLM Systems} \hfill \textbf{Aug 2026 - Present} \vspace{-3pt}
\begin{itemize}
    \item Build Python benchmark scoring 1.2K agent actions across 600 two-agent trials in three competitive task environments
    \item Train three behavioral trace classifiers for deception, collusion, and specification gaming; achieve 0.61 macro-F1 on held-out synthetic traces
    \item Harden evaluation with structured reward, claim-consistency, collusion, and loophole metrics for OpenAI-style and Claude-style agent profiles
    \item Design controlled study matrix spanning eight incentive-pressure settings and configurable opponent profiles to measure strategy-reward tradeoffs
\end{itemize}
```

## Claims to Avoid Until a Live Study Runs

Do not state that the project has benchmarked *OpenAI models* against *Claude
models* yet. The current implementations are scripted, reproducible profiles
named `openai_style` and `claude_style`; they validate the framework, not model
family behavior.

Do not describe the trace classifiers as production-ready or general-purpose.
They are trained and evaluated on a synthetic, deterministic corpus with a
within-generator holdout split.

## What Would Upgrade the Claims

To substantiate a direct OpenAI-versus-Anthropic comparison, run the guarded
live adapters with explicit authorization for API cost, then record the model
IDs, date, prompts, sampling settings, failures, and results. A stronger
classifier claim also needs a separate hand-labeled or independently evaluated
test set.
