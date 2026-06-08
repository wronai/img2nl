"""DSL verb handlers."""

from __future__ import annotations

import json
from typing import Any

from dsl2img2nl.result import DslResult


def handle_analyze(cmd: dict[str, Any], *, line: str) -> DslResult:
    from img2nl import analyze_image

    path = cmd.get("path") or ""
    if not path:
        return DslResult(ok=False, command=line, action="analyze", error="ANALYZE requires image path")
    result = analyze_image(path, locale=cmd.get("locale", "pl"))
    payload = result.to_dict()
    return DslResult(
        ok=result.ok,
        command=line,
        action="analyze",
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
    from img2nl import analyze_image

    path = cmd.get("path") or ""
    if not path:
        return DslResult(ok=False, command=line, action="llm_hint", error="LLM_HINT requires image path")
    result = analyze_image(path, skip_thumbnail=True)
    if not result.ok:
        return DslResult(ok=False, command=line, action="llm_hint", error=result.error)
    payload = result.llm_hint
    return DslResult(
        ok=True,
        command=line,
        action="llm_hint",
        output=json.dumps(payload, ensure_ascii=False, indent=2),
        data=payload,
    )


def handle_from_tokens(line: str, tokens: list[str], cmd: dict[str, Any]) -> DslResult:
    verb = str(cmd.get("verb", "")).upper()
    if verb == "ANALYZE":
        return handle_analyze(cmd, line=line)
    if verb == "QUERY":
        return handle_query(cmd, line=line)
    if verb in {"LLM_HINT", "LLM-HINT"}:
        return handle_llm_hint(cmd, line=line)
    return DslResult(ok=False, command=line, action=verb.lower(), error=f"unknown verb: {verb}")
