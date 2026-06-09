"""DSL verb handlers."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from dsl2img2nl.result import DslResult

VerbHandler = Callable[[dict[str, Any], str], DslResult]


def _require_path(cmd: dict[str, Any], *, line: str, action: str) -> str | None:
    path = cmd.get("path") or cmd.get("out") or ""
    if not path:
        return None
    if "path" not in cmd:
        cmd["path"] = path
    return path


def handle_analyze(cmd: dict[str, Any], *, line: str) -> DslResult:
    from img2nl import api

    if not _require_path(cmd, line=line, action="analyze"):
        return DslResult(ok=False, command=line, action="analyze", error="ANALYZE requires image path")
    result = api.analyze_from_cmd(cmd)
    payload = result.to_dict()
    return DslResult(
        ok=result.ok,
        command=line,
        action="analyze",
        output=result.text or json.dumps(payload, ensure_ascii=False, indent=2),
        data=payload,
        error=result.error,
    )


def handle_targets(cmd: dict[str, Any], *, line: str) -> DslResult:
    from img2nl import api

    if not _require_path(cmd, line=line, action="targets"):
        return DslResult(ok=False, command=line, action="targets", error="TARGETS requires image path")
    payload = api.targets_from_cmd(cmd)
    ok = payload.get("ok", True) is not False and "error" not in payload
    return DslResult(
        ok=ok,
        command=line,
        action="targets",
        output=json.dumps(payload, ensure_ascii=False, indent=2),
        data=payload,
        error=None if ok else payload.get("error"),
    )


def handle_capture(cmd: dict[str, Any], *, line: str) -> DslResult:
    from img2nl import api

    if not _require_path(cmd, line=line, action="capture"):
        return DslResult(ok=False, command=line, action="capture", error="CAPTURE requires OUT path")
    payload = api.capture_from_cmd(cmd)
    return DslResult(
        ok=bool(payload.get("ok")),
        command=line,
        action="capture",
        output=payload.get("path", "") or json.dumps(payload, ensure_ascii=False, indent=2),
        data=payload,
        error=payload.get("error"),
    )


def handle_capture_analyze(cmd: dict[str, Any], *, line: str) -> DslResult:
    from img2nl import api

    if not _require_path(cmd, line=line, action="capture_analyze"):
        return DslResult(
            ok=False,
            command=line,
            action="capture_analyze",
            error="CAPTURE_ANALYZE requires OUT path",
        )
    result = api.capture_analyze_from_cmd(cmd)
    payload = result.to_dict()
    return DslResult(
        ok=result.ok,
        command=line,
        action="capture_analyze",
        output=result.text or json.dumps(payload, ensure_ascii=False, indent=2),
        data=payload,
        error=result.error,
    )


def handle_query(cmd: dict[str, Any], *, line: str) -> DslResult:
    from uri2img2nl.query import query_uri

    uri = cmd.get("uri") or ""
    if not uri and cmd.get("path"):
        from uri2img2nl.uri import uri_for_analyze

        uri = uri_for_analyze(cmd["path"], locale=cmd.get("locale", "pl"))
    if not uri:
        return DslResult(ok=False, command=line, action="query", error="QUERY requires URI or PATH")
    result = query_uri(uri)
    return DslResult(
        ok=result.ok,
        command=line,
        action="query",
        output=result.rendered or "",
        data=result.to_dict(),
        error=result.error,
    )


def handle_llm_hint(cmd: dict[str, Any], *, line: str) -> DslResult:
    from img2nl import api

    if not _require_path(cmd, line=line, action="llm_hint"):
        return DslResult(ok=False, command=line, action="llm_hint", error="LLM_HINT requires image path")
    payload = api.llm_hint_from_path(cmd["path"])
    if payload.get("ok") is False:
        return DslResult(ok=False, command=line, action="llm_hint", error=payload.get("error"))
    return DslResult(
        ok=True,
        command=line,
        action="llm_hint",
        output=json.dumps(payload, ensure_ascii=False, indent=2),
        data=payload,
    )


VERB_HANDLERS: dict[str, VerbHandler] = {
    "ANALYZE": handle_analyze,
    "TARGETS": handle_targets,
    "CAPTURE": handle_capture,
    "CAPTURE_ANALYZE": handle_capture_analyze,
    "QUERY": handle_query,
    "LLM_HINT": handle_llm_hint,
}


def handle_from_tokens(line: str, tokens: list[str], cmd: dict[str, Any]) -> DslResult:
    verb = str(cmd.get("verb", "")).upper().replace("-", "_")
    handler = VERB_HANDLERS.get(verb)
    if handler is None:
        return DslResult(ok=False, command=line, action=verb.lower(), error=f"unknown verb: {verb}")
    return handler(cmd, line=line)
