"""UI element detection via img2vql / imgl."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _from_imgl_elements(elements, *, adapter: str, path: Path) -> dict[str, Any]:
    return {
        "ok": True,
        "path": str(path),
        "adapter": adapter,
        "element_count": len(elements),
        "elements": [
            {
                "id": el.id,
                "role": el.role,
                "bbox": list(el.bbox.as_xyxy()),
                "confidence": el.confidence,
                "label": el.label,
                "metadata": el.metadata,
            }
            for el in elements
        ],
    }


def _try_img2vql(path: Path) -> dict[str, Any] | None:
    try:
        from img2vql import detect_ui_elements
    except ImportError:
        return None
    result = detect_ui_elements(path)
    if not result.get("ok"):
        return None
    result["adapter"] = "img2vql_ui_fast"
    return result


def _try_imgl_bridge(path: Path) -> dict[str, Any] | None:
    try:
        from imgl.detect import detect_with_img2vql
    except ImportError:
        return None
    elements = detect_with_img2vql(path)
    if not elements:
        return None
    return _from_imgl_elements(elements, adapter="imgl_img2vql_bridge", path=path)


def _try_imgl_local(path: Path) -> dict[str, Any] | None:
    try:
        from PIL import Image
        from imgl.detect import detect_ui_elements as imgl_detect_ui
    except ImportError:
        return None
    with Image.open(path) as im:
        elements = imgl_detect_ui(im)
    return _from_imgl_elements(elements, adapter="imgl_ui_fast", path=path)


def analyze_ui_targets(image_path: str | Path, *, prefer_img2vql: bool = True) -> dict[str, Any]:
    path = Path(image_path).expanduser()
    backends = (
        [_try_img2vql, _try_imgl_bridge, _try_imgl_local]
        if prefer_img2vql
        else [_try_imgl_bridge, _try_imgl_local, _try_img2vql]
    )
    for backend in backends:
        result = backend(path)
        if result is not None:
            return result
    return {
        "ok": False,
        "path": str(path),
        "adapter": "ui_fast",
        "error": "ui detection requires img2vql or imgl",
        "elements": [],
    }
