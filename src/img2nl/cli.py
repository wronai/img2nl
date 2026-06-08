"""CLI for img2nl."""

from __future__ import annotations

import argparse
import json
import sys

from img2nl.analyze import analyze_image


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="img2nl", description="Image → NL summary + thumbnail")
    sub = parser.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="Analyze image heuristics")
    a.add_argument("image")
    a.add_argument("--thumbnail", default="")
    a.add_argument(
        "--locale",
        default="pl",
        help="European ISO 639-1 code (pl, en, de, fr, es, cs, uk, ...)",
    )
    a.add_argument("--json", action="store_true")
    a.add_argument("--no-thumbnail", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "analyze":
        result = analyze_image(
            args.image,
            thumbnail=args.thumbnail or None,
            locale=args.locale,
            skip_thumbnail=args.no_thumbnail,
        )
        if args.json:
            print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        else:
            print(result.text)
            if result.thumbnail:
                print(f"thumbnail: {result.thumbnail}")
            print(f"llm: {result.llm_hint.get('recommendation')} ({result.llm_hint.get('confidence')})")
        return 0 if result.ok else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
