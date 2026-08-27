import argparse
import json
from pathlib import Path

from . import __version__
from .artifacts import initialize
from .snapshot import create_snapshot


def build_parser():
    parser = argparse.ArgumentParser(prog="alignment")
    parser.add_argument(
        "--version",
        action="version",
        version=f"epistemic-alignment {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("root", type=Path)
    init_parser.add_argument("--project-id", required=True)
    init_parser.add_argument("--title", required=True)
    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.add_argument("root", type=Path)
    snapshot_parser.add_argument("--json", action="store_true")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init":
        try:
            print(initialize(args.root, args.project_id, args.title))
        except FileExistsError as error:
            parser.error(str(error))
    elif args.command == "snapshot":
        alignment_dir = args.root / "alignment"
        if not alignment_dir.is_dir():
            alignment_dir = args.root
        try:
            snapshot = create_snapshot(alignment_dir)
        except ValueError as error:
            parser.error(str(error))
        if args.json:
            print(json.dumps(snapshot.__dict__, sort_keys=True))
        else:
            print(f"{snapshot.algorithm}:{snapshot.digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
