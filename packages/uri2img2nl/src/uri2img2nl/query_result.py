"""Query result type for img2nl:// URIs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
