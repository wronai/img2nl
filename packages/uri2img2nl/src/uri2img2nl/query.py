"""Query images via img2nl:// URIs."""

from __future__ import annotations

from uri2img2nl.query_handlers import SELECTOR_HANDLERS
from uri2img2nl.query_result import QueryResult
from uri2img2nl.uri import parse_img2nl_uri

__all__ = ["QueryResult", "query_uri"]


def query_uri(uri: str) -> QueryResult:
    try:
        parsed = parse_img2nl_uri(uri)
        handler = SELECTOR_HANDLERS.get(parsed.selector)
        if handler is None:
            return QueryResult(
                ok=False,
                uri=uri,
                selector=parsed.selector,
                path=parsed.path,
                error=f"unknown selector: {parsed.selector}",
            )
        return handler(uri, parsed)
    except Exception as exc:
        return QueryResult(ok=False, uri=uri, selector="", path="", error=str(exc))
