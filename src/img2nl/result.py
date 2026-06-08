"""Result types for img2nl analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Img2NlResult:
    ok: bool
    path: str
    width: int = 0
    height: int = 0
    text: str = ""
    thumbnail: str = ""
    features: dict[str, Any] = field(default_factory=dict)
    llm_hint: dict[str, Any] = field(default_factory=dict)
    locale: str = "pl"
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "path": self.path,
            "width": self.width,
            "height": self.height,
            "text": self.text,
            "thumbnail": self.thumbnail,
            "features": self.features,
            "llm_hint": self.llm_hint,
            "locale": self.locale,
            "error": self.error,
        }
