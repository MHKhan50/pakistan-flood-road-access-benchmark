"""Command-line interface for FloodLink-PK."""

import argparse
import json
from pathlib import Path

from .data import generate_synthetic_rows, write_rows
from .experiment import run_experiment
from .validation import validate_real_data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="floodlink-pk", description="FloodLink-PK reproducible research benchmark")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate a synthetic road-link dataset")
    generate.add_argument("--output", type=Path, default=Path("data/synthetic_segments.csv"))
    generate.add_argument("--scenarios", type=int, default=80)
    generate.add_argument("--segments-per-scenario", type=int, default=50)
    generate.add_argument("--seed", type=int, default=17)

    experiment = subparsers.add_parser("experiment", help="run grouped MLP and graph-access experiments")
    experiment.add_argument("--output-dir", type=Path, default=Path("outputs"))
    experiment.add_argument("--scenarios", type=int, default=80)
    experiment.add_argument("--segments-per-scenario", type=int, default=50)
    experiment.add_argument("--seed", type=int, default=17)
    experiment.add_argument("--epochs", type=int, default=55)

    validate = subparsers.add_parser("validate-real-data", help="validate the required CSV schema")
    validate.add_argument("--input", type=Path, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "generate":
        rows = generate_synthetic_rows(args.scenarios, args.segments_per_scenario, args.seed)
        write_rows(args.output, rows)
        print("Wrote {} synthetic rows to {}".format(len(rows), args.output))
    elif args.command == "experiment":
        metrics = run_experiment(args.output_dir, args.seed, args.scenarios, args.segments_per_scenario, args.epochs)
        print(json.dumps(metrics, indent=2, sort_keys=True))
        print("\nOutputs written to {}".format(args.output_dir))
    elif args.command == "validate-real-data":
        print(json.dumps(validate_real_data(args.input), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
