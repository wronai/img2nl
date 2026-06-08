"""Minimal img2nl DSL parser."""

from __future__ import annotations

import re
import shlex
from typing import Any


def split_command(line: str) -> list[str]:
    return shlex.split(line.strip())


def parse_line(line: str) -> dict[str, Any] | None:
    tokens = split_command(line)
    if not tokens:
        return None
    verb = tokens[0].upper()
    cmd: dict[str, Any] = {"verb": verb}
    i = 1
    while i < len(tokens):
        tok = tokens[i]
        upper = tok.upper()
        if upper == "PATH" and i + 1 < len(tokens):
            cmd["path"] = tokens[i + 1]
            i += 2
            continue
        if upper == "LOCALE" and i + 1 < len(tokens):
            cmd["locale"] = tokens[i + 1]
            i += 2
            continue
        if upper == "URI" and i + 1 < len(tokens):
            cmd["uri"] = tokens[i + 1]
            i += 2
            continue
        if upper == "OUT" and i + 1 < len(tokens):
            cmd["out"] = tokens[i + 1]
            i += 2
            continue
        if "path" not in cmd and not tok.startswith("img2nl://"):
            cmd["path"] = tok
        elif tok.startswith("img2nl://"):
            cmd["uri"] = tok
        i += 1
    return cmd
