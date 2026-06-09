"""Per-selector handlers for img2nl:// URIs."""

from __future__ import annotations

import json
from collections.abc import Callable

from uri2img2nl.query_result import QueryResult
from uri2img2nl.uri import Img2NlUri

SelectorHandler = Callable[[str, Img2NlUri], QueryResult]


def cmd_from_uri(parsed: Img2NlUri) -> dict:
    return {
        "path": parsed.path,
        "locale": parsed.locale,
        "source_type": parsed.source_type,
        "goal": parsed.goal,
        "targets": parsed.targets,
        "profile": parsed.profile,
        "monitor": parsed.monitor,
        "backend": parsed.backend,
        "speed": parsed.speed,
        "enable_ui_detect": parsed.enable_ui_detect,
        "enable_detect": parsed.enable_detect,
        "out": parsed.path,
    }


def _missing_path(uri: str, parsed: Img2NlUri, *, param: str = "path=") -> QueryResult:
    return QueryResult(
        ok=False,
        uri=uri,
        selector=parsed.selector,
        path="",
        error=f"missing {param} query parameter",
    )


def _analyze_failure(uri: str, parsed: Img2NlUri, error: str | None) -> QueryResult:
    return QueryResult(
        ok=False,
        uri=uri,
        selector=parsed.selector,
        path=parsed.path,
        error=error,
    )


def handle_capture_analyze(uri: str, parsed: Img2NlUri) -> QueryResult:
    from img2nl import api

    if not parsed.path:
        return _missing_path(uri, parsed, param="out=")
    result = api.capture_analyze_from_cmd(cmd_from_uri(parsed))
    if not result.ok:
        return _analyze_failure(uri, parsed, result.error)
    payload = result.to_dict()
    return QueryResult(
        ok=True,
        uri=uri,
        selector=parsed.selector,
        path=result.path,
        data=payload,
        rendered=json.dumps(payload, ensure_ascii=False, indent=2),
        keys=["text", "targets", "features", "capture", "llm_hint"],
    )


def handle_targets(uri: str, parsed: Img2NlUri) -> QueryResult:
    from img2nl import api

    if not parsed.path:
        return _missing_path(uri, parsed)
    payload = api.targets_from_cmd(cmd_from_uri(parsed))
    if payload.get("ok") is False or payload.get("error"):
        return _analyze_failure(uri, parsed, payload.get("error"))
    return QueryResult(
        ok=True,
        uri=uri,
        selector=parsed.selector,
        path=parsed.path,
        data=payload,
        rendered=json.dumps(payload, ensure_ascii=False, indent=2),
        keys=["targets", "presence", "identifications", "hit_count"],
    )


def handle_analyze(uri: str, parsed: Img2NlUri) -> QueryResult:
    from img2nl import api

    if not parsed.path:
        return _missing_path(uri, parsed)
    result = api.analyze_from_cmd(cmd_from_uri(parsed))
    if not result.ok:
        return _analyze_failure(uri, parsed, result.error)
    payload = result.to_dict()
    return QueryResult(
        ok=True,
        uri=uri,
        selector=parsed.selector,
        path=parsed.path,
        data=payload,
        rendered=json.dumps(payload, ensure_ascii=False, indent=2),
        keys=["text", "thumbnail", "features", "targets", "llm_hint"],
    )


def handle_llm_hint(uri: str, parsed: Img2NlUri) -> QueryResult:
    from img2nl import api

    if not parsed.path:
        return _missing_path(uri, parsed)
    payload = api.llm_hint_from_path(parsed.path)
    if payload.get("ok") is False:
        return _analyze_failure(uri, parsed, payload.get("error"))
    return QueryResult(
        ok=True,
        uri=uri,
        selector=parsed.selector,
        path=parsed.path,
        data=payload,
        rendered=json.dumps(payload, ensure_ascii=False, indent=2),
    )


def handle_text(uri: str, parsed: Img2NlUri) -> QueryResult:
    from img2nl import api

    if not parsed.path:
        return _missing_path(uri, parsed)
    try:
        text = api.text_from_path(parsed.path, locale=parsed.locale)
    except RuntimeError as exc:
        return _analyze_failure(uri, parsed, str(exc))
    return QueryResult(
        ok=True,
        uri=uri,
        selector=parsed.selector,
        path=parsed.path,
        data={"text": text},
        rendered=text,
    )


SELECTOR_HANDLERS: dict[str, SelectorHandler] = {
    "capture-analyze": handle_capture_analyze,
    "capture_analyze": handle_capture_analyze,
    "targets": handle_targets,
    "analyze": handle_analyze,
    "": handle_analyze,
    "llm-hint": handle_llm_hint,
    "llm_hint": handle_llm_hint,
    "text": handle_text,
}
