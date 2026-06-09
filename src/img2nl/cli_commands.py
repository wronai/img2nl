"""CLI subcommand executors."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from img2nl.analyze import analyze_image


def _target_list(raw: str) -> list[str] | None:
    values = [t.strip() for t in raw.split(",") if t.strip()]
    return values or None


def _profile_kwargs(cmd: dict[str, Any]) -> dict[str, Any]:
    from img2nl.profiles import analyze_kwargs_from_cmd

    return analyze_kwargs_from_cmd(cmd)


def cmd_analyze(args: argparse.Namespace) -> int:
    target_list = _target_list(args.targets)
    profile_kw = _profile_kwargs(
        {
            "profile": args.profile,
            "source_type": args.source_type,
            "goal": args.goal,
            "targets": ",".join(target_list) if target_list else "",
            "speed": args.speed,
            "enable_ui_detect": args.enable_ui_detect,
            "enable_detect": args.enable_detect,
            "locale": args.locale,
            "no_thumbnail": args.no_thumbnail,
        }
    )
    result = analyze_image(
        args.image,
        thumbnail=args.thumbnail or None,
        translate_mode=args.translate_mode,
        **profile_kw,
    )
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.text)
        if result.thumbnail:
            print(f"thumbnail: {result.thumbnail}")
        print(f"source: {result.source_type} goal: {result.goal}")
        if result.targets.get("hit_count"):
            print(f"targets: {result.targets['hit_count']}/{result.targets.get('target_count', 0)}")
        print(f"llm: {result.llm_hint.get('recommendation')} ({result.llm_hint.get('confidence')})")
    return 0 if result.ok else 1


def cmd_capture(args: argparse.Namespace) -> int:
    from img2nl.capture import capture_screenshot

    result = capture_screenshot(args.output, monitor=args.monitor, backend=args.backend)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif result.get("ok"):
        print(result["path"])
    else:
        print(result.get("error", "capture failed"), file=sys.stderr)
    return 0 if result.get("ok") else 1


def cmd_capture_analyze(args: argparse.Namespace) -> int:
    from img2nl.capture import capture_and_analyze

    target_list = _target_list(args.targets)
    profile_kw = _profile_kwargs(
        {
            "profile": args.profile,
            "goal": args.goal,
            "targets": ",".join(target_list) if target_list else "",
            "enable_detect": args.enable_detect,
            "locale": args.locale,
            "no_thumbnail": args.no_thumbnail,
        }
    )
    result = capture_and_analyze(
        args.output,
        monitor=args.monitor,
        backend=args.backend,
        click_target=args.click_target or None,
        execute_click=args.execute_click,
        **profile_kw,
    )
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(result.text)
        if result.capture:
            print(f"capture: {result.capture.get('backend')} -> {result.path}")
        if result.targets.get("hit_count"):
            print(f"targets: {result.targets['hit_count']}/{result.targets.get('target_count', 0)}")
        if result.click_result:
            cr = result.click_result
            print(f"click: {cr.get('method')} ok={cr.get('ok')} {cr.get('message', cr.get('error', ''))}")
    return 0 if result.ok else 1


def cmd_translate_install(args: argparse.Namespace) -> int:
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
