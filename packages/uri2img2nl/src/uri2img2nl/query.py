"""Query images via img2nl:// URIs."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from uri2img2nl.uri import parse_img2nl_uri


@dataclass
class QueryResult:
    ok: bool
    uri: str
    selector: str
    path: str
    data: Any = None
    rendered: str = ""
    error: str | None = None
    keys: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "uri": self.uri,
            "selector": self.selector,
            "path": self.path,
            "data": self.data,
            "rendered": self.rendered,
            "keys": self.keys,
            "error": self.error,
        }


def query_uri(uri: str) -> QueryResult:
    from img2nl import analyze_image

    try:
        parsed = parse_img2nl_uri(uri)
        if not parsed.path:
            return QueryResult(
                ok=False,
                uri=uri,
                selector=parsed.selector,
                path="",
                error="missing path= query parameter",
            )

        if parsed.selector in {"analyze", ""}:
            result = analyze_image(parsed.path, locale=parsed.locale)
            if not result.ok:
                return QueryResult(
                    ok=False,
                    uri=uri,
                    selector=parsed.selector,
                    path=parsed.path,
                    error=result.error,
                )
            payload = result.to_dict()
            return QueryResult(
                ok=True,
                uri=uri,
                selector=parsed.selector,
                path=parsed.path,
                data=payload,
                rendered=json.dumps(payload, ensure_ascii=False, indent=2),
                keys=["text", "thumbnail", "features", "llm_hint"],
            )

        if parsed.selector in {"llm-hint", "llm_hint"}:
            result = analyze_image(parsed.path, skip_thumbnail=True)
            if not result.ok:
                return QueryResult(ok=False, uri=uri, selector=parsed.selector, path=parsed.path, error=result.error)
            payload = result.llm_hint
            return QueryResult(
                ok=True,
                uri=uri,
                selector=parsed.selector,
                path=parsed.path,
                data=payload,
                rendered=json.dumps(payload, ensure_ascii=False, indent=2),
            )

        if parsed.selector == "text":
            result = analyze_image(parsed.path, skip_thumbnail=True, locale=parsed.locale)
            if not result.ok:
                return QueryResult(ok=False, uri=uri, selector=parsed.selector, path=parsed.path, error=result.error)
            return QueryResult(
                ok=True,
                uri=uri,
                selector=parsed.selector,
                path=parsed.path,
                data={"text": result.text},
                rendered=result.text,
            )

        return QueryResult(
            ok=False,
            uri=uri,
            selector=parsed.selector,
            path=parsed.path,
            error=f"unknown selector: {parsed.selector}",
        )
    except Exception as exc:
        return QueryResult(ok=False, uri=uri, selector="", path="", error=str(exc))
