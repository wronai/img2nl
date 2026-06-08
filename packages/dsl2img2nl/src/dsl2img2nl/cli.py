"""CLI for dsl2img2nl."""

from __future__ import annotations

import argparse
import json
import sys

from dsl2img2nl import dispatch


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dsl2img2nl")
    parser.add_argument("-c", "--command", default="")
    parser.add_argument("file", nargs="?", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    line = args.command
    if not line and args.file:
        line = open(args.file, encoding="utf-8").read().strip()
    if not line:
        line = sys.stdin.read().strip()
    result = dispatch(line)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.output or result.error or "")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
