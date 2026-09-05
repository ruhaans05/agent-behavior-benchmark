from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark import run_benchmark, save_run
from .study import run_initial_study, save_study


def main() -> None:
    parser = argparse.ArgumentParser(prog="agent-bench")
    subcommands = parser.add_subparsers(dest="command", required=True)

    run = subcommands.add_parser("run", help="Run a benchmark experiment.")
    run.add_argument("--experiment", default="starter", choices=["starter", "negotiation", "resource_allocation", "auction"])
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

    args = parser.parse_args()
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


def _print_summary(summary: dict[str, dict[str, float]]) -> None:
    for provider, metrics in summary.items():
        print(f"\n{provider}")
        for key in sorted(metrics):
            print(f"  {key}: {metrics[key]}")


if __name__ == "__main__":
    main()
