"""Parse and build img2nl:// URIs."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qs, urlencode, urlparse

IMG2NL_SCHEME = "img2nl"


@dataclass
class Img2NlUri:
    scheme: str
    selector: str
    path: str = ""
    locale: str = "pl"

    @property
    def target(self) -> str:
        return f"{self.scheme}://{self.selector}"


def is_img2nl_uri(uri: str) -> bool:
    return urlparse(uri).scheme.lower() == IMG2NL_SCHEME


def uri_for_analyze(path: str, *, locale: str = "pl", thumbnail: str = "") -> str:
    params: dict[str, str] = {"path": path, "locale": locale}
    if thumbnail:
        params["thumbnail"] = thumbnail
    return f"img2nl://analyze?{urlencode(params)}"


def uri_for_llm_hint(path: str) -> str:
    return f"img2nl://llm-hint?{urlencode({'path': path})}"


def parse_img2nl_uri(uri: str) -> Img2NlUri:
    parsed = urlparse(uri)
    if parsed.scheme != IMG2NL_SCHEME:
        raise ValueError(f"expected img2nl:// URI, got: {uri}")
    selector = (parsed.netloc + parsed.path).strip("/") or "analyze"
    qs = parse_qs(parsed.query)
    path = (qs.get("path") or [""])[0]
    locale = (qs.get("locale") or ["pl"])[0]
    return Img2NlUri(scheme=IMG2NL_SCHEME, selector=selector, path=path, locale=locale)
