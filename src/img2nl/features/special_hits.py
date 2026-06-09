"""Orchestrate conditional specialist detectors (layer 3)."""

from __future__ import annotations

from typing import Any

from img2nl.features.barcodes import analyze_barcodes
from img2nl.features.ocr_text import analyze_ocr


def analyze_special_hits(im, features: dict[str, Any]) -> dict[str, Any]:
    barcodes = analyze_barcodes(im, features=features)
    ocr = analyze_ocr(im, features=features)
    return {
        "barcodes": barcodes,
        "ocr": ocr,
        "has_qr": barcodes.get("has_codes", False),
        "has_text": ocr.get("has_text", False),
    }
