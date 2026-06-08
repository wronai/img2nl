"""Thin shell wrapper over dsl2img2nl."""

from __future__ import annotations

import argparse
import json
import sys

from dsl2img2nl import dispatch


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cli2img2nl")
    sub = parser.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("exec", help="Execute one DSL line")
    e.add_argument("line")
    e.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    if args.cmd == "exec":
        result = dispatch(args.line)
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(result.output or result.error or "")
        return 0 if result.ok else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
