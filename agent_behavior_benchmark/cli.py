from __future__ import annotations

import argparse
from pathlib import Path

from .benchmark import run_benchmark, save_run


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


def _print_summary(summary: dict[str, dict[str, float]]) -> None:
    for provider, metrics in summary.items():
        print(f"\n{provider}")
        for key in sorted(metrics):
            print(f"  {key}: {metrics[key]}")


if __name__ == "__main__":
    main()

