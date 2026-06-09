"""Execute target analysis from an execution plan."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from img2nl.features.identify_matchers import identify_from_features
from img2nl.features.presence_matchers import presence_from_features
from img2nl.features.targets import build_target_report
from img2nl.features.ui_adapter import analyze_ui_targets
from img2nl.plan import ExecutionPlan


def execute_target_plan(
    image_path: str | Path,
    features: dict[str, Any],
    plan: ExecutionPlan,
) -> dict[str, Any]:
    if plan.run_ui_detect:
        features["ui_targets"] = analyze_ui_targets(image_path)

    presence = presence_from_features(features, plan.resolved_targets)
    identifications = (
        identify_from_features(features, plan.resolved_targets)
        if plan.run_identify
        else []
    )

    report = build_target_report(presence, identifications)
    report.update(
        {
            "source_type": plan.source_type,
            "goal": plan.goal,
            "speed": plan.speed,
            "resolved_targets": plan.resolved_targets,
            "adapters": _active_adapters(features, plan=plan),
        }
    )
    return report


def _active_adapters(features: dict[str, Any], *, plan: ExecutionPlan) -> list[str]:
    adapters = ["heuristic_presence", "barcode_fast", "ocr_fast"]
    if plan.run_ui_detect:
        adapters.append(features.get("ui_targets", {}).get("adapter", "ui_fast"))
    if features.get("semantic_hits", {}).get("objects"):
        adapters.append("semantic_fast")
    return adapters


# Backward-compatible aliases
def analyze_targets(
    image_path: str | Path,
    features: dict[str, Any],
    *,
    source_type: str = "photo",
    goal: str = "describe",
    targets: list[str] | None = None,
    speed: str = "fast",
    enable_ui_detect: bool = False,
    enable_detect: bool = False,
) -> dict[str, Any]:
    from img2nl.plan import build_execution_plan

    size = features.get("colors", {}).get("size", [0, 0])
    plan = build_execution_plan(
        explicit_source=source_type,  # type: ignore[arg-type]
        goal=goal,  # type: ignore[arg-type]
        targets=targets,
        speed=speed,  # type: ignore[arg-type]
        enable_detect=enable_detect,
        enable_ui_detect=enable_ui_detect,
        width=int(size[0]) if size else 0,
        height=int(size[1]) if size else 0,
        features=features,
    )
    return execute_target_plan(image_path, features, plan)


def resolve_targets(*, source_type: str, goal: str, targets: list[str] | None) -> list[str]:
    from img2nl.plan import resolve_targets as _resolve

    return _resolve(source_type=source_type, goal=goal, targets=targets)  # type: ignore[arg-type]


def should_run_ui_detect(*, source_type: str, goal: str, explicit: bool) -> bool:
    from img2nl.plan import should_run_ui_detect as _should

    return _should(source_type=source_type, goal=goal, explicit=explicit)  # type: ignore[arg-type]


def should_run_semantic(*, source_type: str, goal: str, speed: str, enable_detect: bool) -> bool:
    from img2nl.plan import should_run_semantic as _should

    return _should(
        source_type=source_type,
        goal=goal,  # type: ignore[arg-type]
        speed=speed,  # type: ignore[arg-type]
        enable_detect=enable_detect,
    )
