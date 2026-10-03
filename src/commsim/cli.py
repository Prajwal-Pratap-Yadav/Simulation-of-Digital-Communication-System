"""One entry point for configured communication experiments."""

import argparse
from pathlib import Path

from . import __version__
from .experiments import Config, run


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run theory-checked communication experiments"
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("--config", type=Path, default=Path("configs/default.json"))
    parser.add_argument("--output", type=Path, default=Path("reports"))
    args = parser.parse_args()
    try:
        rows = run(Config.load(args.config), args.output)
    except (ValueError, TypeError, KeyError, OSError) as exc:
        parser.error(str(exc))
    print(f"Recorded {len(rows)} BER points in {args.output}; see run_manifest.json")


if __name__ == "__main__":
    main()
