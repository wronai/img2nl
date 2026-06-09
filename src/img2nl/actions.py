"""Desktop click automation from target analysis."""

from __future__ import annotations

from typing import Any

from img2nl.features.targets import find_click_point
from img2nl.result import Img2NlResult


def build_click_action(
    target_report: dict[str, Any],
    target: str,
    *,
    button: int = 1,
) -> dict[str, Any] | None:
    point = find_click_point(target_report, target)
    if not point:
        return None
    x, y = int(round(point[0])), int(round(point[1]))
    return {"action": "click", "x": x, "y": y, "target": target, "button": button}


def execute_click_action(
    action: dict[str, Any],
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    try:
        from imgl.execute import execute_action

        result = execute_action(action, dry_run=dry_run)
        return {
            "ok": result.ok,
            "method": result.method,
            "message": result.message,
            "dry_run": result.dry_run,
            "action": action,
        }
    except ImportError:
        pass

    try:
        from vdisplay.input import LinuxXdotoolInput

        if dry_run:
            return {
                "ok": True,
                "method": "dry-run",
                "message": f"click @ ({action['x']}, {action['y']})",
                "dry_run": True,
                "action": action,
            }
        inp = LinuxXdotoolInput()
        inp.move(int(action["x"]), int(action["y"]))
        inp.click(int(action.get("button", 1)))
        return {
            "ok": True,
            "method": "vdisplay-xdotool",
            "message": f"click @ ({action['x']}, {action['y']})",
            "dry_run": False,
            "action": action,
        }
    except ImportError:
        return {
            "ok": False,
            "method": "none",
            "message": "No click backend (install imgl or vdisplay with xdotool)",
            "dry_run": dry_run,
            "action": action,
        }
    except Exception as exc:
        return {
            "ok": False,
            "method": "vdisplay-xdotool",
            "message": str(exc),
            "dry_run": dry_run,
            "action": action,
        }


def click_target(
    target_report: dict[str, Any],
    target: str,
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    action = build_click_action(target_report, target)
    if action is None:
        return {"ok": False, "error": f"target not found: {target}"}
    return execute_click_action(action, dry_run=dry_run)


def click_from_result(
    result: Img2NlResult,
    target: str,
    *,
    dry_run: bool = True,
) -> dict[str, Any]:
    if not result.ok:
        return {"ok": False, "error": result.error or "analysis failed"}
    report = result.targets or result.features.get("target_analysis", {})
    return click_target(report, target, dry_run=dry_run)
