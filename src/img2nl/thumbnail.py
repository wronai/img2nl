"""Thumbnail generation for LLM/API transport."""

from __future__ import annotations

from pathlib import Path


def make_thumbnail(
    image_path: str | Path,
    *,
    out: str | Path | None = None,
    max_size: int = 256,
    quality: int = 82,
) -> str:
    from PIL import Image

    src = Path(image_path).expanduser()
    if not src.is_file():
        raise FileNotFoundError(f"image not found: {src}")

    dst = Path(out or src.with_name(f"{src.stem}.thumb.jpg"))
    dst.parent.mkdir(parents=True, exist_ok=True)

    im = Image.open(src)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    im.thumbnail((max_size, max_size))
    im.save(dst, format="JPEG", quality=quality, optimize=True)
    return str(dst)
