"""Screenshot capture via vdisplay (preferred) or imgl fallback."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from img2nl.analyze import analyze_image
from img2nl.context import AnalysisGoal, SourceType, SpeedMode
from img2nl.result import Img2NlResult


def capture_screenshot(
    output: str | Path,
    *,
    monitor: int = 1,
    backend: str = "auto",
) -> dict[str, Any]:
    path = Path(output).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    if backend in {"auto", "vdisplay"}:
        try:
            from vdisplay.application.services.capture import capture_screenshot as vd_capture

            meta = vd_capture(output=str(path), monitor=monitor)
            saved = meta.get("saved") or meta.get("path") or str(path)
            return {"ok": True, "path": str(saved), "backend": "vdisplay", "meta": meta}
        except ImportError:
            if backend == "vdisplay":
                return {
                    "ok": False,
                    "path": str(path),
                    "backend": "vdisplay",
                    "error": "vdisplay not installed: pip install -e /path/to/vdisplay[pillow]",
                }
        except Exception as exc:
            if backend == "vdisplay":
                return {"ok": False, "path": str(path), "backend": "vdisplay", "error": str(exc)}

    if backend in {"auto", "imgl"}:
        try:
            from imgl.capture import capture_screen

            saved = capture_screen(path, monitor=monitor)
            return {"ok": True, "path": str(saved), "backend": "imgl", "meta": {"monitor": monitor}}
        except ImportError:
            return {
                "ok": False,
                "path": str(path),
                "backend": "imgl",
                "error": "imgl not installed: pip install -e /path/to/imgl[capture]",
            }
        except Exception as exc:
            return {"ok": False, "path": str(path), "backend": "imgl", "error": str(exc)}

    return {"ok": False, "path": str(path), "backend": backend, "error": f"unknown backend: {backend}"}


def capture_and_analyze(
    output: str | Path,
    *,
    monitor: int = 1,
    backend: str = "auto",
    source_type: SourceType = "screenshot",
    goal: AnalysisGoal = "click",
    targets: list[str] | None = None,
    speed: SpeedMode = "fast",
    enable_ui_detect: bool = True,
    click_target: str | None = None,
    execute_click: bool = False,
    **analyze_kw: Any,
) -> Img2NlResult:
    capture = capture_screenshot(output, monitor=monitor, backend=backend)
    if not capture.get("ok"):
        return Img2NlResult(
            ok=False,
            path=str(capture.get("path", output)),
            error=capture.get("error", "capture failed"),
            capture=capture,
        )

    result = analyze_image(
        capture["path"],
        source_type=source_type,
        goal=goal,
        targets=targets,
        speed=speed,
        enable_ui_detect=enable_ui_detect,
        **analyze_kw,
    )
    result.capture = capture
    if click_target:
        from img2nl.actions import click_from_result

        result.click_result = click_from_result(
            result,
            click_target,
            dry_run=not execute_click,
        )
    return result
