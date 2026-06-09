"""Minimal img2nl DSL parser."""

from __future__ import annotations

import shlex
from collections.abc import Callable
from typing import Any

TokenStep = Callable[[dict[str, Any], list[str], int], int | None]


def split_command(line: str) -> list[str]:
    return shlex.split(line.strip())


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _normalize_token(token: str) -> str:
    return token.upper().replace("-", "_")


def _set_pair(cmd: dict[str, Any], tokens: list[str], index: int, key: str) -> int:
    cmd[key] = tokens[index + 1]
    return index + 2


def _consume_kv(
    cmd: dict[str, Any],
    tokens: list[str],
    index: int,
    *,
    key: str,
    converter: Callable[[str], Any] | None = None,
) -> int:
    value: Any = tokens[index + 1]
    if converter is not None:
        value = converter(value)
    cmd[key] = value
    return index + 2


_KV_SPECS: dict[str, tuple[str, Callable[[str], Any] | None]] = {
    "PATH": ("path", None),
    "OUT": ("out", None),
    "OUTPUT": ("out", None),
    "LOCALE": ("locale", None),
    "URI": ("uri", None),
    "GOAL": ("goal", None),
    "SOURCE": ("source_type", None),
    "SOURCE_TYPE": ("source_type", None),
    "PROFILE": ("profile", None),
    "BACKEND": ("backend", None),
    "SPEED": ("speed", None),
    "TARGETS": ("targets", None),
    "MONITOR": ("monitor", int),
}

_BOOL_FLAGS = frozenset({"ENABLE_UI", "ENABLE_UI_DETECT", "ENABLE_DETECT", "NO_THUMBNAIL"})
_FLAG_STOP_WORDS = frozenset({"path", "out", "goal", "source"})


def _try_kv_token(cmd: dict[str, Any], tokens: list[str], index: int) -> int | None:
    upper = _normalize_token(tokens[index])
    spec = _KV_SPECS.get(upper)
    if spec is None or index + 1 >= len(tokens):
        return None
    key, converter = spec
    return _consume_kv(cmd, tokens, index, key=key, converter=converter)


def _try_bool_flag(cmd: dict[str, Any], tokens: list[str], index: int) -> int | None:
    upper = _normalize_token(tokens[index])
    if upper not in _BOOL_FLAGS:
        return None
    key = upper.lower()
    if index + 1 < len(tokens) and tokens[index + 1].lower() not in _FLAG_STOP_WORDS:
        cmd[key] = _parse_bool(tokens[index + 1])
        return index + 2
    cmd[key] = True
    return index + 1


def _apply_positional(cmd: dict[str, Any], tokens: list[str], index: int) -> int:
    tok = tokens[index]
    if "path" not in cmd and not tok.startswith("img2nl://"):
        cmd["path"] = tok
    elif tok.startswith("img2nl://"):
        cmd["uri"] = tok
    return index + 1


_TOKEN_STEPS: tuple[TokenStep, ...] = (_try_kv_token, _try_bool_flag)


def _consume_token(cmd: dict[str, Any], tokens: list[str], index: int) -> int:
    for step in _TOKEN_STEPS:
        if next_index := step(cmd, tokens, index):
            return next_index
    return _apply_positional(cmd, tokens, index)


def _finalize_cmd(cmd: dict[str, Any]) -> dict[str, Any]:
    if "out" in cmd and "path" not in cmd:
        cmd["path"] = cmd["out"]
    return cmd


def parse_line(line: str) -> dict[str, Any] | None:
    tokens = split_command(line)
    if not tokens:
        return None
    cmd: dict[str, Any] = {"verb": _normalize_token(tokens[0])}
    index = 1
    while index < len(tokens):
        index = _consume_token(cmd, tokens, index)
    return _finalize_cmd(cmd)
