"""Registry of identification collectors."""

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

IdentifyCollector = Callable[[dict[str, Any], list[str]], list[TargetDetection]]


def collect_barcodes(features: dict[str, Any], targets: list[str]) -> list[TargetDetection]:
    if "qrcode" not in targets:
        return []
    barcodes = features.get("special_hits", {}).get("barcodes", {})
    if not barcodes.get("has_codes"):
        return []
    return [
        TargetDetection(
            target="qrcode",
            present=True,
            confidence=0.95,
            adapter="barcode_fast",
            detection_type="identify",
            label=str(code.get("type", "code")),
            bbox=list(code.get("bbox", [])),
            metadata={"data": code.get("data", "")},
        )
        for code in barcodes.get("codes", [])
    ]


def collect_ocr(features: dict[str, Any], targets: list[str]) -> list[TargetDetection]:
    if "text" not in targets:
        return []
    ocr = features.get("special_hits", {}).get("ocr", {})
    if not ocr.get("has_text"):
        return []
    return [
        TargetDetection(
            target="text",
            present=True,
            confidence=0.75,
            adapter="ocr_fast",
            detection_type="identify",
            label=ocr.get("text_preview", "text"),
            metadata={"line_count": ocr.get("line_count", 0)},
        )
    ]


def collect_ui(features: dict[str, Any], targets: list[str]) -> list[TargetDetection]:
    ui = features.get("ui_targets", {})
    if not ui.get("ok"):
        return []
    hits: list[TargetDetection] = []
    for element in ui.get("elements", []):
        role = str(element.get("role", ""))
        label = str(element.get("label", ""))
        for target in targets:
            if not match_ui_role(target, label, role):
                continue
            hits.append(
                TargetDetection(
                    target=target,
                    present=True,
                    confidence=float(element.get("confidence", 0.5)),
                    adapter=ui.get("adapter", "ui_fast"),
                    detection_type="identify",
                    label=label or role,
                    bbox=list(element.get("bbox", [])),
                    metadata={
                        "role": role,
                        "location": element.get("location", ""),
                        "center": element.get("center", []),
                    },
                )
            )
    return hits


def collect_semantic(features: dict[str, Any], targets: list[str]) -> list[TargetDetection]:
    hits: list[TargetDetection] = []
    wanted = SEMANTIC_TARGETS.intersection(targets)
    if not wanted:
        return hits
    for obj in features.get("semantic_hits", {}).get("objects", []):
        name = str(obj.get("label", "")).lower()
        for target in wanted:
            if target == "animal" and name not in ANIMAL_LABELS:
                continue
            if target == "bird" and name not in BIRD_LABELS:
                continue
            if target not in {"animal", "bird"} and name != target:
                continue
            hits.append(
                TargetDetection(
                    target=target,
                    present=True,
                    confidence=float(obj.get("confidence", 0.5)),
                    adapter="semantic_fast",
                    detection_type="identify",
                    label=name,
                    bbox=list(obj.get("bbox", [])),
                )
            )
    return hits


IDENTIFY_COLLECTORS: tuple[IdentifyCollector, ...] = (
    collect_barcodes,
    collect_ocr,
    collect_ui,
    collect_semantic,
)


def identify_from_features(
    features: dict[str, Any],
    targets: list[str],
) -> list[TargetDetection]:
    hits: list[TargetDetection] = []
    for collector in IDENTIFY_COLLECTORS:
        hits.extend(collector(features, targets))
    return hits
