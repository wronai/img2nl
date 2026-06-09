"""Object detection via ultralytics YOLO (optional, layer 4)."""

from __future__ import annotations

from typing import Any

_MODEL = None


def _should_detect(features: dict[str, Any], *, send_to_llm: bool) -> bool:
    if not send_to_llm:
        return False
    scene = features.get("scene", {})
    return scene.get("scene_class") != "empty_dark_screen"


def _get_model():
    global _MODEL
    if _MODEL is None:
        from ultralytics import YOLO

        _MODEL = YOLO("yolov8n.pt")
    return _MODEL


def analyze_semantic(
    im,
    *,
    features: dict[str, Any],
    send_to_llm: bool = False,
    max_labels: int = 8,
    conf: float = 0.35,
) -> dict[str, Any]:
    if not _should_detect(features, send_to_llm=send_to_llm):
        return {
            "available": True,
            "skipped": True,
            "reason": "trigger_not_met",
            "model": None,
            "labels": [],
            "objects": [],
            "object_count": 0,
        }

    try:
        from ultralytics import YOLO  # noqa: F401
    except ImportError:
        return {
            "available": False,
            "reason": "ultralytics not installed: pip install img2nl[detect]",
            "model": None,
            "labels": [],
            "objects": [],
            "object_count": 0,
        }

    rgb = im.convert("RGB")
    model = _get_model()
    results = model.predict(source=rgb, verbose=False, conf=conf)
    objects: list[dict[str, Any]] = []
    labels: list[str] = []
    for result in results:
        names = result.names or {}
        if result.boxes is None:
            continue
        for box in result.boxes:
            cls_id = int(box.cls.item())
            name = names.get(cls_id, str(cls_id))
            conf_val = float(box.conf.item())
            xyxy = [round(float(v), 1) for v in box.xyxy[0].tolist()]
            objects.append({"label": name, "confidence": round(conf_val, 3), "bbox": xyxy})
            if name not in labels:
                labels.append(name)

    labels = labels[:max_labels]
    objects = objects[: max_labels * 2]
    return {
        "available": True,
        "skipped": False,
        "model": "yolov8n.pt",
        "labels": labels,
        "objects": objects,
        "object_count": len(objects),
    }
