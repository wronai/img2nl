"""img2nl:// URI layer."""

from uri2img2nl.query import QueryResult, query_uri
from uri2img2nl.uri import (
    is_img2nl_uri,
    uri_for_analyze,
    uri_for_capture_analyze,
    uri_for_llm_hint,
    uri_for_targets,
)

__all__ = [
    "QueryResult",
    "query_uri",
    "is_img2nl_uri",
    "uri_for_analyze",
    "uri_for_capture_analyze",
    "uri_for_llm_hint",
    "uri_for_targets",
]
