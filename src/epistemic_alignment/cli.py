import argparse

from . import __version__


def build_parser():
    parser = argparse.ArgumentParser(prog="alignment")
    parser.add_argument(
        "--version",
        action="version",
        version=f"epistemic-alignment {__version__}",
    )
    return parser


def main(argv=None):
    build_parser().parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
