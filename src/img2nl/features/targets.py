"""Unified target detection result format (presence + identification)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TargetDetection:
    target: str
    present: bool
    confidence: float = 0.0
    adapter: str = ""
    detection_type: str = "presence"
    label: str = ""
    bbox: list[float] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "present": self.present,
            "confidence": round(self.confidence, 3),
            "adapter": self.adapter,
            "detection_type": self.detection_type,
            "label": self.label,
            "bbox": self.bbox,
            "metadata": self.metadata,
        }


def best_detection(target_report: dict[str, Any], target: str) -> dict[str, Any] | None:
    """Return highest-confidence detection for automation (click/type)."""
    best: dict[str, Any] | None = None
    best_score = -1.0
    for hit in target_report.get("targets", []):
        if hit.get("target") != target or not hit.get("present"):
            continue
        for det in hit.get("detections", []):
            score = float(det.get("confidence", 0.0))
            if score > best_score:
                best_score = score
                best = det
        if best is None and hit.get("bbox"):
            best = {
                "target": target,
                "confidence": float(hit.get("confidence", 0.0)),
                "bbox": hit.get("bbox", []),
                "center": _bbox_center(hit.get("bbox", [])),
            }
    return best


def find_click_point(target_report: dict[str, Any], target: str) -> tuple[float, float] | None:
    det = best_detection(target_report, target)
    if not det:
        return None
    center = det.get("center")
    if isinstance(center, (list, tuple)) and len(center) >= 2:
        return float(center[0]), float(center[1])
    bbox = det.get("bbox", [])
    if len(bbox) >= 4:
        return _bbox_center(bbox)
    return None


def _bbox_center(bbox: list[float]) -> tuple[float, float]:
    if len(bbox) < 4:
        return (0.0, 0.0)
    x0, y0, x1, y1 = bbox[:4]
    return ((x0 + x1) / 2.0, (y0 + y1) / 2.0)


def build_target_report(
    presence: list[TargetDetection],
    identifications: list[TargetDetection],
) -> dict[str, Any]:
    by_target: dict[str, dict[str, Any]] = {}
    for hit in presence:
        by_target.setdefault(hit.target, {"target": hit.target})
        by_target[hit.target]["present"] = hit.present
        by_target[hit.target]["confidence"] = round(hit.confidence, 3)
        by_target[hit.target]["adapter"] = hit.adapter
    for hit in identifications:
        entry = by_target.setdefault(
            hit.target,
            {"target": hit.target, "present": True, "confidence": 0.0, "adapter": hit.adapter},
        )
        entry.setdefault("detections", []).append(hit.to_dict())
        if hit.present:
            entry["present"] = True
            entry["confidence"] = max(float(entry.get("confidence", 0.0)), hit.confidence)

    hits = list(by_target.values())
    return {
        "hit_count": sum(1 for h in hits if h.get("present")),
        "target_count": len(hits),
        "presence": [p.to_dict() for p in presence],
        "identifications": [i.to_dict() for i in identifications],
        "targets": hits,
    }
