import argparse
from pathlib import Path

from . import __version__
from .artifacts import initialize


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
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init":
        try:
            print(initialize(args.root, args.project_id, args.title))
        except FileExistsError as error:
            parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
