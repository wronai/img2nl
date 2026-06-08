"""Single dispatch entry for img2nl DSL."""

from __future__ import annotations

from typing import Any

from dsl2img2nl.grammar import parse_line, split_command
from dsl2img2nl.handlers import handle_from_tokens
from dsl2img2nl.result import DslResult


def dispatch(envelope: str | dict[str, Any], *, default_path: str | None = None) -> DslResult:
    if isinstance(envelope, dict):
        line = envelope.get("line") or str(envelope)
        cmd = envelope
    else:
        line = str(envelope).strip()
        cmd = parse_line(line) or {"verb": split_command(line)[0].upper() if line else "NOOP"}

    if not line:
        return DslResult(ok=True, command="", action="noop")
    if default_path and "path" not in cmd:
        cmd["path"] = default_path
    tokens = split_command(line)
    return handle_from_tokens(line, tokens, cmd)


def execute_dsl_line(line: str, *, default_path: str | None = None) -> DslResult:
    return dispatch(line, default_path=default_path)
