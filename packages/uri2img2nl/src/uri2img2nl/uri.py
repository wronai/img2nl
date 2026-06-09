"""Parse and build img2nl:// URIs."""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import parse_qs, urlencode, urlparse

IMG2NL_SCHEME = "img2nl"


@dataclass
class Img2NlUri:
    scheme: str
    selector: str
    path: str = ""
    locale: str = "pl"
    source_type: str = "auto"
    goal: str = "describe"
    targets: str = ""
    profile: str = ""
    monitor: int = 1
    backend: str = "auto"
    speed: str = "fast"
    enable_ui_detect: bool = False
    enable_detect: bool = False
    extra: dict[str, str] = field(default_factory=dict)

    @property
    def target(self) -> str:
        return f"{self.scheme}://{self.selector}"


def is_img2nl_uri(uri: str) -> bool:
    return urlparse(uri).scheme.lower() == IMG2NL_SCHEME


def _encode_params(params: dict[str, str | int | bool]) -> str:
    encoded: dict[str, str] = {}
    for key, value in params.items():
        if value in ("", None):
            continue
        if isinstance(value, bool):
            encoded[key] = "1" if value else "0"
        else:
            encoded[key] = str(value)
    return urlencode(encoded)


def uri_for_analyze(
    path: str,
    *,
    locale: str = "pl",
    thumbnail: str = "",
    source_type: str = "auto",
    goal: str = "describe",
    targets: str = "",
    profile: str = "",
    enable_ui_detect: bool = False,
    enable_detect: bool = False,
    speed: str = "fast",
) -> str:
    params: dict[str, str | int | bool] = {
        "path": path,
        "locale": locale,
        "source_type": source_type,
        "goal": goal,
        "speed": speed,
        "enable_ui_detect": enable_ui_detect,
        "enable_detect": enable_detect,
    }
    if thumbnail:
        params["thumbnail"] = thumbnail
    if targets:
        params["targets"] = targets
    if profile:
        params["profile"] = profile
    return f"img2nl://analyze?{_encode_params(params)}"


def uri_for_targets(
    path: str,
    *,
    goal: str = "click",
    targets: str = "button,input,qrcode,text",
    profile: str = "fast_ui",
) -> str:
    params = {
        "path": path,
        "goal": goal,
        "targets": targets,
        "profile": profile,
        "enable_ui_detect": True,
    }
    return f"img2nl://targets?{_encode_params(params)}"


def uri_for_capture_analyze(
    out: str,
    *,
    monitor: int = 1,
    backend: str = "auto",
    goal: str = "click",
    profile: str = "fast_ui",
) -> str:
    params = {
        "out": out,
        "monitor": monitor,
        "backend": backend,
        "goal": goal,
        "profile": profile,
        "enable_ui_detect": True,
    }
    return f"img2nl://capture-analyze?{_encode_params(params)}"


def uri_for_llm_hint(path: str) -> str:
    return f"img2nl://llm-hint?{urlencode({'path': path})}"


def _bool_param(qs: dict[str, list[str]], key: str) -> bool:
    raw = (qs.get(key) or ["0"])[0]
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def parse_img2nl_uri(uri: str) -> Img2NlUri:
    parsed = urlparse(uri)
    if parsed.scheme != IMG2NL_SCHEME:
        raise ValueError(f"expected img2nl:// URI, got: {uri}")
    selector = (parsed.netloc + parsed.path).strip("/") or "analyze"
    qs = parse_qs(parsed.query)
    path = (qs.get("path") or qs.get("out") or [""])[0]
    locale = (qs.get("locale") or ["pl"])[0]
    return Img2NlUri(
        scheme=IMG2NL_SCHEME,
        selector=selector,
        path=path,
        locale=locale,
        source_type=(qs.get("source_type") or ["auto"])[0],
        goal=(qs.get("goal") or ["describe"])[0],
        targets=(qs.get("targets") or [""])[0],
        profile=(qs.get("profile") or [""])[0],
        monitor=int((qs.get("monitor") or ["1"])[0]),
        backend=(qs.get("backend") or ["auto"])[0],
        speed=(qs.get("speed") or ["fast"])[0],
        enable_ui_detect=_bool_param(qs, "enable_ui_detect"),
        enable_detect=_bool_param(qs, "enable_detect"),
        extra={k: v[0] for k, v in qs.items()},
    )
