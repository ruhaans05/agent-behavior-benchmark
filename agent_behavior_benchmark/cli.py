from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark import run_benchmark, save_run
from .config import load_local_env
from .demo import run_dialogue_demo, save_dialogue_demo
from .dialogue_study import run_dialogue_study, save_dialogue_study, save_dialogue_study_aggregate
from .live_study import run_live_study
from .live_dialogue_study import run_live_dialogue_pilot, run_live_extended_dialogue_pilot, save_public_dialogue_aggregate
from .live_analysis import analyze_live_trace, save_live_analysis, validate_live_trace
from .study import run_initial_study, save_study


def main() -> None:
    parser = argparse.ArgumentParser(prog="agent-bench")
    subcommands = parser.add_subparsers(dest="command", required=True)

    run = subcommands.add_parser("run", help="Run a benchmark experiment.")
    run.add_argument("--experiment", default="starter", choices=["starter", "negotiation", "negotiation_dialogue", "negotiation_dialogue_extended", "resource_allocation", "auction"])
    run.add_argument("--providers", nargs="+", default=["openai_style", "claude_style"])
    run.add_argument("--trials", type=int, default=25)
    run.add_argument("--seed", type=int, default=7)
    run.add_argument("--allow-live", action="store_true")
    run.add_argument("--output-dir", default="runs")

    report = subcommands.add_parser("report", help="Print a run summary.")
    report.add_argument("path")

    study = subcommands.add_parser("study", help="Run the reproducible simulated baseline study.")
    study.add_argument("--trials-per-environment", type=int, default=200)
    study.add_argument("--seed", type=int, default=20260905)
    study.add_argument("--output", default="results/initial_simulated_baseline.json")

    live_study = subcommands.add_parser("live-study", help="Run a metered round-robin API study.")
    live_study.add_argument("--phase", choices=["pilot", "full"], default="pilot")
    live_study.add_argument("--seed", type=int, default=20260907)
    live_study.add_argument("--output-dir", default="live_runs")
    live_study.add_argument("--max-actions", type=int, default=54)

    live_dialogue = subcommands.add_parser("live-dialogue-pilot", help="Run a capped live two-model dialogue pilot.")
    live_dialogue.add_argument("--seed", type=int, default=20260907)
    live_dialogue.add_argument("--output-dir", default="live_runs")
    live_dialogue.add_argument("--max-model-calls", type=int, default=32)
    live_dialogue.add_argument("--models", nargs=2, default=["openai:gpt-5-mini", "anthropic:claude-sonnet-5"])
    live_dialogue.add_argument("--public-output", default=None)

    live_interaction = subcommands.add_parser("live-interaction-pilot", help="Run a capped six-turn live interaction pilot.")
    live_interaction.add_argument("--seed", type=int, default=20260908)
    live_interaction.add_argument("--output-dir", default="live_runs")
    live_interaction.add_argument("--max-model-calls", type=int, default=24)
    live_interaction.add_argument("--models", nargs=2, default=["openai:gpt-5-mini", "openai:gpt-5.4-mini-2026-03-17"])
    live_interaction.add_argument("--public-output", default=None)

    live_report = subcommands.add_parser("live-report", help="Aggregate a checkpointed live-study trace without exporting transcripts.")
    live_report.add_argument("trace_path")
    live_report.add_argument("--output", default="live_runs/live-analysis.json")

    live_verify = subcommands.add_parser("live-verify", help="Validate a checkpoint against its frozen study schedule.")
    live_verify.add_argument("trace_path")
    live_verify.add_argument("--phase", choices=["pilot", "full"], default="full")
    live_verify.add_argument("--seed", type=int, default=20260907)

    demo = subcommands.add_parser("demo", help="Run a no-cost multi-turn negotiation walkthrough.")
    demo.add_argument("--seed", type=int, default=7)
    demo.add_argument("--output", default=None)

    dialogue_study = subcommands.add_parser("dialogue-study", help="Run the no-cost controlled dialogue factorial study.")
    dialogue_study.add_argument("--repeats", type=int, default=25)
    dialogue_study.add_argument("--seed", type=int, default=20260907)
    dialogue_study.add_argument("--output", default="results/controlled_dialogue_study.json")
    dialogue_study.add_argument("--summary-output", default=None)

    args = parser.parse_args()
    load_local_env()
    if args.command == "run":
        payload = run_benchmark(args.experiment, args.providers, args.trials, args.seed, args.allow_live)
        path = save_run(payload, Path(args.output_dir))
        print(f"Saved run: {path}")
        _print_summary(payload["summary"])
    elif args.command == "report":
        from .benchmark import load_run

        payload = load_run(Path(args.path))
        _print_summary(payload["summary"])
    elif args.command == "study":
        payload = run_initial_study(args.trials_per_environment, args.seed)
        path = save_study(payload, Path(args.output))
        print(f"Saved study: {path}")
        print(f"Environment trials: {payload['environment_trials']}")
        print(f"Agent actions: {payload['agent_actions']}")
        for label, metrics in payload["behavior_classifier_metrics"].items():
            print(f"  {label} F1: {metrics['f1']}")
    elif args.command == "live-study":
        payload = run_live_study(args.phase, args.seed, Path(args.output_dir), args.max_actions)
        print(f"Saved {payload['phase']} study with {payload['agent_actions']} agent actions.")
        _print_summary(payload["summary"])
    elif args.command == "live-dialogue-pilot":
        payload = run_live_dialogue_pilot(
            args.seed,
            Path(args.output_dir),
            args.max_model_calls,
            models=tuple(args.models),
        )
        if args.public_output:
            public_path = save_public_dialogue_aggregate(payload, Path(args.public_output))
            print(f"Saved transcript-free aggregate: {public_path}")
        print(f"Saved live dialogue pilot with {payload['completed_trials']} trials and {payload['completed_model_calls']} model calls.")
        for condition, metrics in payload["condition_outcomes"].items():
            print(f"  {condition}: agreement={metrics['agreement_rate']}, conflict={metrics['conflict_rate']}")
    elif args.command == "live-interaction-pilot":
        payload = run_live_extended_dialogue_pilot(
            args.seed,
            Path(args.output_dir),
            args.max_model_calls,
            models=tuple(args.models),
        )
        if args.public_output:
            public_path = save_public_dialogue_aggregate(payload, Path(args.public_output))
            print(f"Saved transcript-free aggregate: {public_path}")
        print(f"Saved live interaction pilot with {payload['completed_trials']} trials and {payload['completed_model_calls']} model calls.")
        for condition, metrics in payload["condition_outcomes"].items():
            print(f"  {condition}: agreement={metrics['agreement_rate']}, revisions={metrics['mean_revised_offers']}")
    elif args.command == "live-report":
        payload = analyze_live_trace(Path(args.trace_path))
        path = save_live_analysis(payload, Path(args.output))
        print(f"Saved live analysis: {path}")
        print(f"Completed trials: {payload['completed_trials']}")
        print(f"Completed agent actions: {payload['completed_agent_actions']}")
        _print_summary(payload["overall"])
    elif args.command == "live-verify":
        payload = validate_live_trace(Path(args.trace_path), args.phase, args.seed)
        print(f"Checkpoint valid: {payload['valid']}")
        print(f"Completed trials: {payload['completed_trials']} / {payload['scheduled_trials']}")
        if payload["issues"]:
            for issue in payload["issues"]:
                print(f"  issue: {issue}")
            raise SystemExit(1)
    elif args.command == "demo":
        _, markdown = run_dialogue_demo(args.seed)
        if args.output:
            path = save_dialogue_demo(markdown, Path(args.output))
            print(f"Saved dialogue demo: {path}")
        print(markdown)
    elif args.command == "dialogue-study":
        payload = run_dialogue_study(args.repeats, args.seed)
        path = save_dialogue_study(payload, Path(args.output))
        print(f"Saved dialogue study: {path}")
        if args.summary_output:
            summary_path = save_dialogue_study_aggregate(payload, Path(args.summary_output))
            print(f"Saved transcript-free aggregate: {summary_path}")
        print(f"Environment trials: {payload['environment_trials']}")
        print(f"Conversation turns: {payload['conversation_turns']}")
        for key, metrics in payload["summary"].items():
            print(f"  {key}: agreement={metrics['agreement']}, conflict={metrics['conflict']}")


def _print_summary(summary: dict[str, dict[str, float]]) -> None:
    for provider, metrics in summary.items():
        print(f"\n{provider}")
        for key in sorted(metrics):
            print(f"  {key}: {metrics[key]}")


if __name__ == "__main__":
    main()
