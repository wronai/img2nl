"""Execution plan: which features and adapters to run."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from img2nl.context import AnalysisGoal, SourceType, SpeedMode, default_targets, infer_source_type

_UI_GOALS = {"find", "click", "index"}
_UI_SOURCES = {"screenshot", "document"}
_IDENTIFY_GOALS = {"find", "click", "index"}
_TEXT_TARGETS = frozenset({"qrcode", "text", "barcode"})
_ALL_BASE_LAYERS = frozenset(
    {"colors", "dynamics", "noise", "objects", "patterns", "edges", "fingerprint"}
)


@dataclass
class ExecutionPlan:
    source_type: str
    goal: AnalysisGoal
    speed: SpeedMode
    resolved_targets: list[str]
    run_ui_detect: bool
    run_semantic: bool
    run_identify: bool
    base_layers: frozenset[str]
    run_special_hits: bool


def resolve_targets(
    *,
    source_type: str,
    goal: AnalysisGoal,
    targets: list[str] | None,
) -> list[str]:
    resolved = list(targets or default_targets(source_type))
    if goal == "click" and "button" not in resolved:
        resolved.insert(0, "button")
    if goal == "click" and "input" not in resolved:
        resolved.insert(1, "input")
    return resolved


def should_run_ui_detect(
    *,
    source_type: SourceType,
    goal: AnalysisGoal,
    explicit: bool,
) -> bool:
    if explicit:
        return True
    return source_type in _UI_SOURCES or goal in _UI_GOALS


def should_run_semantic(
    *,
    source_type: str,
    goal: AnalysisGoal,
    speed: SpeedMode,
    enable_detect: bool,
) -> bool:
    if enable_detect:
        return True
    if speed == "fast" and goal in _IDENTIFY_GOALS and source_type == "photo":
        return True
    return speed == "full"


def should_run_identify(*, goal: AnalysisGoal, speed: SpeedMode) -> bool:
    return goal in _IDENTIFY_GOALS or speed != "fast"


def resolve_base_layers(
    *,
    source_type: str,
    goal: AnalysisGoal,
    speed: SpeedMode,
    resolved_targets: list[str],
    run_semantic: bool,
) -> frozenset[str]:
    if goal == "describe" or speed == "full":
        return _ALL_BASE_LAYERS

    target_set = set(resolved_targets)

    if source_type == "screenshot" and goal in _UI_GOALS:
        layers = {"colors", "objects", "patterns"}
        if target_set & _TEXT_TARGETS:
            layers.update({"edges", "dynamics"})
        return frozenset(layers)

    if source_type == "document":
        return frozenset({"colors", "edges", "patterns", "objects", "dynamics"})

    layers = {"colors", "objects"}
    if target_set & _TEXT_TARGETS:
        layers.add("dynamics")
    if speed == "balanced" or run_semantic:
        layers.update({"patterns", "edges", "noise"})
    if speed == "balanced":
        layers.add("dynamics")
    return frozenset(layers)


def should_run_special_hits(
    *,
    goal: AnalysisGoal,
    source_type: str,
    resolved_targets: list[str],
    speed: SpeedMode,
) -> bool:
    if goal == "describe":
        return True
    if source_type == "document":
        return True
    if set(resolved_targets) & _TEXT_TARGETS:
        return True
    return speed != "fast"


def build_execution_plan(
    *,
    explicit_source: SourceType,
    goal: AnalysisGoal,
    targets: list[str] | None,
    speed: SpeedMode,
    enable_detect: bool,
    enable_ui_detect: bool,
    width: int,
    height: int,
    features: dict[str, Any],
) -> ExecutionPlan:
    source_type = infer_source_type(
        explicit=explicit_source,
        width=width,
        height=height,
        features=features,
    )
    resolved_targets = resolve_targets(
        source_type=source_type,
        goal=goal,
        targets=targets,
    )
    run_ui = should_run_ui_detect(
        source_type=source_type,  # type: ignore[arg-type]
        goal=goal,
        explicit=enable_ui_detect,
    )
    run_semantic = should_run_semantic(
        source_type=source_type,
        goal=goal,
        speed=speed,
        enable_detect=enable_detect,
    )
    return ExecutionPlan(
        source_type=source_type,
        goal=goal,
        speed=speed,
        resolved_targets=resolved_targets,
        run_ui_detect=run_ui,
        run_semantic=run_semantic,
        run_identify=should_run_identify(goal=goal, speed=speed),
        base_layers=resolve_base_layers(
            source_type=source_type,
            goal=goal,
            speed=speed,
            resolved_targets=resolved_targets,
            run_semantic=run_semantic,
        ),
        run_special_hits=should_run_special_hits(
            goal=goal,
            source_type=source_type,
            resolved_targets=resolved_targets,
            speed=speed,
        ),
    )
