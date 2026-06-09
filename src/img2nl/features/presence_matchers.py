"""Registry of per-target presence matchers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from img2nl.features.matchers_common import (
    ANIMAL_LABELS,
    BIRD_LABELS,
    SEMANTIC_TARGETS,
    match_ui_role,
)
from img2nl.features.targets import TargetDetection

PresenceMatcher = Callable[[dict[str, Any], str], TargetDetection | None]


def _absent(target: str) -> TargetDetection:
    return TargetDetection(target=target, present=False, adapter="heuristic")


def _best_semantic_object(features: dict[str, Any], target: str) -> dict[str, Any] | None:
    for obj in features.get("semantic_hits", {}).get("objects", []):
        name = str(obj.get("label", "")).lower()
        if target == "person" and name == "person":
            return obj
        if target == "animal" and name in ANIMAL_LABELS:
            return obj
        if target == "bird" and name in BIRD_LABELS:
            return obj
        if target == name:
            return obj
    return None


def match_qrcode(features: dict[str, Any], target: str) -> TargetDetection | None:
    if target != "qrcode":
        return None
    barcodes = features.get("special_hits", {}).get("barcodes", {})
    if not barcodes.get("has_codes"):
        return None
    return TargetDetection(
        target=target,
        present=True,
        confidence=0.95,
        adapter="barcode_fast",
        label="qrcode",
    )


def match_text(features: dict[str, Any], target: str) -> TargetDetection | None:
    if target != "text":
        return None
    ocr = features.get("special_hits", {}).get("ocr", {})
    if not ocr.get("has_text"):
        return None
    return TargetDetection(
        target=target,
        present=True,
        confidence=0.8,
        adapter="ocr_fast",
        label=ocr.get("text_preview", "text"),
    )


def match_semantic(features: dict[str, Any], target: str) -> TargetDetection | None:
    if target not in SEMANTIC_TARGETS:
        return None
    obj = _best_semantic_object(features, target)
    if not obj:
        return None
    return TargetDetection(
        target=target,
        present=True,
        confidence=float(obj.get("confidence", 0.5)),
        adapter="semantic_fast",
        label=str(obj.get("label", target)),
        bbox=list(obj.get("bbox", [])),
    )


def match_ui(features: dict[str, Any], target: str) -> TargetDetection | None:
    ui = features.get("ui_targets", {})
    if not ui.get("ok"):
        return None

    best_conf = 0.0
    label = ""
    bbox: list[float] = []
    for element in ui.get("elements", []):
        role = str(element.get("role", ""))
        el_label = str(element.get("label", ""))
        if not match_ui_role(target, el_label, role):
            continue
        conf = float(element.get("confidence", 0.5))
        if conf >= best_conf:
            best_conf = conf
            label = el_label or role
            bbox = list(element.get("bbox", []))

    if best_conf <= 0.0:
        return None
    return TargetDetection(
        target=target,
        present=True,
        confidence=best_conf,
        adapter=ui.get("adapter", "ui_fast"),
        label=label,
        bbox=bbox,
    )


PRESENCE_MATCHERS: tuple[PresenceMatcher, ...] = (
    match_qrcode,
    match_text,
    match_semantic,
    match_ui,
)


def presence_from_features(
    features: dict[str, Any],
    targets: list[str],
) -> list[TargetDetection]:
    hits: list[TargetDetection] = []
    for target in targets:
        hit: TargetDetection | None = None
        for matcher in PRESENCE_MATCHERS:
            hit = matcher(features, target)
            if hit is not None:
                break
        hits.append(hit if hit is not None else _absent(target))
    return hits
