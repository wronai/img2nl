"""CLI for img2nl."""

from __future__ import annotations

import argparse

from img2nl.cli_commands import (
    cmd_analyze,
    cmd_capture,
    cmd_capture_analyze,
    cmd_translate_install,
)


def _add_analyze_parser(sub: argparse._SubParsersAction) -> None:
    parser = sub.add_parser("analyze", help="Analyze image heuristics")
    parser.add_argument("image")
    parser.add_argument("--thumbnail", default="")
    parser.add_argument("--locale", default="pl")
    parser.add_argument(
        "--translate-mode",
        default="auto",
        choices=["auto", "catalog", "offline"],
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-thumbnail", action="store_true")
    parser.add_argument(
        "--source-type",
        default="auto",
        choices=["auto", "photo", "screenshot", "document", "camera"],
    )
    parser.add_argument(
        "--goal",
        default="describe",
        choices=["describe", "find", "click", "index"],
    )
    parser.add_argument("--targets", default="")
    parser.add_argument("--speed", default="fast", choices=["fast", "balanced", "full"])
    parser.add_argument("--enable-ui-detect", action="store_true")
    parser.add_argument("--enable-detect", action="store_true")
    parser.add_argument(
        "--profile",
        default="",
        choices=["", "fast_ui", "fast_photo", "fast_document", "full_desktop"],
    )
    parser.set_defaults(func=cmd_analyze)


def _add_capture_parser(sub: argparse._SubParsersAction) -> None:
    parser = sub.add_parser("capture", help="Capture screenshot via vdisplay or imgl")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--monitor", type=int, default=1)
    parser.add_argument("--backend", default="auto", choices=["auto", "vdisplay", "imgl"])
    parser.add_argument("--json", action="store_true")
    parser.set_defaults(func=cmd_capture)


def _add_capture_analyze_parser(sub: argparse._SubParsersAction) -> None:
    parser = sub.add_parser("capture-analyze", help="Capture screenshot and analyze it")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--monitor", type=int, default=1)
    parser.add_argument("--backend", default="auto", choices=["auto", "vdisplay", "imgl"])
    parser.add_argument("--locale", default="pl")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--no-thumbnail", action="store_true")
    parser.add_argument("--goal", default="click", choices=["describe", "find", "click", "index"])
    parser.add_argument("--targets", default="")
    parser.add_argument("--enable-detect", action="store_true")
    parser.add_argument(
        "--profile",
        default="fast_ui",
        choices=["fast_ui", "fast_photo", "fast_document", "full_desktop"],
    )
    parser.set_defaults(func=cmd_capture_analyze)


def _add_translate_install_parser(sub: argparse._SubParsersAction) -> None:
    parser = sub.add_parser("translate-install", help="Install argostranslate language pair")
    parser.add_argument("from_lang", nargs="?", default="en")
    parser.add_argument("to_lang", nargs="?", default="pl")
    parser.add_argument("--list-available", action="store_true")
    parser.add_argument("--list-installed", action="store_true")
    parser.set_defaults(func=cmd_translate_install)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="img2nl", description="Image → NL summary + thumbnail")
    sub = parser.add_subparsers(dest="cmd", required=True)
    _add_analyze_parser(sub)
    _add_capture_parser(sub)
    _add_capture_analyze_parser(sub)
    _add_translate_install_parser(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
