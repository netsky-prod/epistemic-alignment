import argparse
import json
from pathlib import Path

from . import __version__
from .approval import check_gate, issue_review, record_decision
from .artifacts import initialize
from .handoff import write_handoff
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
    issue_parser = subparsers.add_parser("issue-review")
    issue_parser.add_argument("root", type=Path)
    issue_parser.add_argument("--adapter", required=True)
    issue_parser.add_argument("--status", required=True)
    issue_parser.add_argument("--location", required=True)
    decide_parser = subparsers.add_parser("decide")
    decide_parser.add_argument("root", type=Path)
    decide_parser.add_argument("--decision", required=True)
    decide_parser.add_argument("--reviewer", required=True)
    decide_parser.add_argument("--provenance", required=True)
    decide_parser.add_argument("--review-hash", required=True)
    decide_parser.add_argument("--acknowledged-finding", action="append", default=[])
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("root", type=Path)
    check_parser.add_argument("--json", action="store_true")
    handoff_parser = subparsers.add_parser("handoff")
    handoff_parser.add_argument("root", type=Path)
    return parser


def _alignment_dir(root: Path) -> Path:
    alignment_dir = root / "alignment"
    return alignment_dir if alignment_dir.is_dir() else root


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "init":
        try:
            print(initialize(args.root, args.project_id, args.title))
        except FileExistsError as error:
            parser.error(str(error))
    elif args.command == "snapshot":
        alignment_dir = _alignment_dir(args.root)
        try:
            snapshot = create_snapshot(alignment_dir)
        except ValueError as error:
            parser.error(str(error))
        if args.json:
            print(json.dumps(snapshot.__dict__, sort_keys=True))
        else:
            print(f"{snapshot.algorithm}:{snapshot.digest}")
    elif args.command == "issue-review":
        try:
            snapshot = issue_review(
                _alignment_dir(args.root), args.adapter, args.status, args.location
            )
        except ValueError as error:
            parser.error(str(error))
        print(f"{snapshot.algorithm}:{snapshot.digest}")
    elif args.command == "decide":
        try:
            record_decision(
                _alignment_dir(args.root),
                args.decision,
                args.reviewer,
                args.provenance,
                args.review_hash,
                args.acknowledged_finding,
            )
        except ValueError as error:
            parser.error(str(error))
        print("decision recorded")
    elif args.command == "check":
        gate = check_gate(_alignment_dir(args.root))
        if args.json:
            print(json.dumps(gate.__dict__, sort_keys=True))
        else:
            print(f"{gate.digest}: {'ready' if gate.ready else ', '.join(gate.reasons)}")
        return 0 if gate.ready else 1
    elif args.command == "handoff":
        try:
            print(write_handoff(_alignment_dir(args.root)))
        except ValueError as error:
            parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
