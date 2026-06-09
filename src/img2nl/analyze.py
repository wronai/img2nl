"""Full image analysis pipeline."""

from __future__ import annotations

from pathlib import Path

from img2nl.context import AnalysisGoal, SourceType, SpeedMode
from img2nl.describe import TranslateMode, describe_image
from img2nl.features.extractors import apply_semantic_layer, extract_base_features
from img2nl.features.router import execute_target_plan
from img2nl.i18n import normalize_locale
from img2nl.llm_gate import llm_transport_hint
from img2nl.plan import build_execution_plan
from img2nl.result import Img2NlResult
from img2nl.thumbnail import make_thumbnail


def _require_pillow() -> str | None:
    try:
        import PIL  # noqa: F401
    except ImportError:
        return "pillow required: pip install img2nl[analyze]"
    return None


def _open_image(path: Path):
    from PIL import Image

    return Image.open(path)


def _assemble_result(
    *,
    path: Path,
    width: int,
    height: int,
    features: dict,
    plan,
    locale: str,
    translate_mode: TranslateMode,
    thumbnail: str | Path | None,
    thumbnail_max: int,
    skip_thumbnail: bool,
) -> Img2NlResult:
    text = describe_image(features, locale=locale, translate_mode=translate_mode)
    llm_hint = llm_transport_hint(features)
    thumb_path = ""
    if not skip_thumbnail:
        thumb_path = make_thumbnail(path, out=thumbnail, max_size=thumbnail_max)
    return Img2NlResult(
        ok=True,
        path=str(path),
        width=width,
        height=height,
        text=text,
        thumbnail=thumb_path,
        features=features,
        llm_hint=llm_hint,
        locale=locale,
        source_type=plan.source_type,
        goal=plan.goal,
        targets=features.get("target_analysis", {}),
    )


def analyze_image(
    image_path: str | Path,
    *,
    thumbnail: str | Path | None = None,
    thumbnail_max: int = 256,
    locale: str = "pl",
    translate_mode: TranslateMode = "auto",
    skip_thumbnail: bool = False,
    reference_fingerprint: dict | None = None,
    enable_detect: bool = False,
    source_type: SourceType = "auto",
    goal: AnalysisGoal = "describe",
    targets: list[str] | None = None,
    speed: SpeedMode = "fast",
    enable_ui_detect: bool = False,
) -> Img2NlResult:
    if err := _require_pillow():
        return Img2NlResult(ok=False, path=str(image_path), error=err)

    path = Path(image_path).expanduser()
    if not path.is_file():
        return Img2NlResult(ok=False, path=str(path), error=f"image not found: {path}")

    try:
        im = _open_image(path)
        w, h = im.size
        features = extract_base_features(im, reference_fingerprint=reference_fingerprint)
        plan = build_execution_plan(
            explicit_source=source_type,
            goal=goal,
            targets=targets,
            speed=speed,
            enable_detect=enable_detect,
            enable_ui_detect=enable_ui_detect,
            width=w,
            height=h,
            features=features,
        )
        apply_semantic_layer(im, features, enabled=plan.run_semantic)
        features["target_analysis"] = execute_target_plan(path, features, plan)

        return _assemble_result(
            path=path,
            width=w,
            height=h,
            features=features,
            plan=plan,
            locale=normalize_locale(locale),
            translate_mode=translate_mode,
            thumbnail=thumbnail,
            thumbnail_max=thumbnail_max,
            skip_thumbnail=skip_thumbnail,
        )
    except Exception as exc:
        return Img2NlResult(ok=False, path=str(path), error=str(exc))
