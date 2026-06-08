"""Message catalog for European locales."""

from __future__ import annotations

import json
from pathlib import Path

_CATALOG_PATH = Path(__file__).with_name("messages.json")


def _load_messages() -> dict[str, dict[str, str]]:
    data = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    return {key: bucket for key, bucket in data.items()}


MESSAGES: dict[str, dict[str, str]] = _load_messages()
