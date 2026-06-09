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
    a.add_argument(
        "--translate-mode",
        default="auto",
        choices=["auto", "catalog", "offline"],
        help="auto=catalog pl/en + argostranslate en→target; offline=require argos; catalog=static JSON only",
    )
    a.add_argument("--json", action="store_true")
    a.add_argument("--no-thumbnail", action="store_true")

    ti = sub.add_parser("translate-install", help="Install argostranslate language pair (offline)")
    ti.add_argument("from_lang", nargs="?", default="en")
    ti.add_argument("to_lang", nargs="?", default="pl")
    ti.add_argument("--list-available", action="store_true")
    ti.add_argument("--list-installed", action="store_true")

    args = parser.parse_args(argv)

    if args.cmd == "analyze":
        result = analyze_image(
            args.image,
            thumbnail=args.thumbnail or None,
            locale=args.locale,
            translate_mode=args.translate_mode,
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

    if args.cmd == "translate-install":
        from img2nl.i18n.offline import (
            argostranslate_available,
            ensure_language_pair,
            list_available_pairs,
            list_installed_pairs,
        )

        if not argostranslate_available():
            print("Install: pip install img2nl[translate]")
            return 1
        if args.list_installed:
            for pair in list_installed_pairs():
                print(f"{pair[0]} -> {pair[1]}")
            return 0
        if args.list_available:
            for pair in list_available_pairs(refresh_index=True):
                print(f"{pair[0]} -> {pair[1]}")
            return 0
        ok = ensure_language_pair(args.from_lang, args.to_lang, refresh_index=True)
        print(f"{'ok' if ok else 'failed'}: {args.from_lang} -> {args.to_lang}")
        return 0 if ok else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
