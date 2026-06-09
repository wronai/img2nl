"""Thin facade for DSL/URI adapter packages — single import surface."""

from __future__ import annotations

from typing import Any

from img2nl.actions import click_from_result
from img2nl.analyze import analyze_image
from img2nl.capture import capture_and_analyze, capture_screenshot
from img2nl.profiles import analyze_kwargs_from_cmd
from img2nl.result import Img2NlResult


def analyze_from_cmd(cmd: dict[str, Any]) -> Img2NlResult:
    return analyze_image(cmd["path"], **analyze_kwargs_from_cmd(cmd))


def targets_from_cmd(cmd: dict[str, Any]) -> dict[str, Any]:
    kwargs = analyze_kwargs_from_cmd(cmd)
    kwargs.setdefault("goal", "find")
    kwargs.setdefault("enable_ui_detect", True)
    kwargs["skip_thumbnail"] = True
    result = analyze_image(cmd["path"], **kwargs)
    if not result.ok:
        return {"ok": False, "error": result.error}
    return result.targets or result.features.get("target_analysis", {})


def capture_from_cmd(cmd: dict[str, Any]) -> dict[str, Any]:
    out = cmd.get("out") or cmd.get("path") or ""
    return capture_screenshot(
        out,
        monitor=int(cmd.get("monitor", 1)),
        backend=str(cmd.get("backend", "auto")),
    )


def capture_analyze_from_cmd(cmd: dict[str, Any]) -> Img2NlResult:
    out = cmd.get("out") or cmd.get("path") or ""
    kwargs = analyze_kwargs_from_cmd(cmd)
    kwargs.setdefault("source_type", "screenshot")
    kwargs.setdefault("goal", "click")
    kwargs.setdefault("enable_ui_detect", True)
    click_target_name = cmd.get("click_target") or cmd.get("click")
    execute_click = bool(cmd.get("execute_click") or cmd.get("execute"))
    return capture_and_analyze(
        out,
        monitor=int(cmd.get("monitor", 1)),
        backend=str(cmd.get("backend", "auto")),
        click_target=str(click_target_name) if click_target_name else None,
        execute_click=execute_click,
        **kwargs,
    )


def click_target_from_cmd(cmd: dict[str, Any]) -> dict[str, Any]:
    kwargs = analyze_kwargs_from_cmd(cmd)
    kwargs.setdefault("goal", "click")
    kwargs.setdefault("enable_ui_detect", True)
    kwargs["skip_thumbnail"] = True
    result = analyze_image(cmd["path"], **kwargs)
    target = str(cmd.get("click_target") or cmd.get("target") or "button")
    dry_run = not bool(cmd.get("execute_click") or cmd.get("execute"))
    return click_from_result(result, target, dry_run=dry_run)


def llm_hint_from_path(path: str) -> dict[str, Any]:
    result = analyze_image(path, skip_thumbnail=True)
    if not result.ok:
        return {"ok": False, "error": result.error}
    return result.llm_hint


def text_from_path(path: str, *, locale: str = "pl") -> str:
    result = analyze_image(path, skip_thumbnail=True, locale=locale)
    if not result.ok:
        raise RuntimeError(result.error or "analyze failed")
    return result.text
