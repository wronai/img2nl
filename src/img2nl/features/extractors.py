"""Base heuristic feature extraction."""

from __future__ import annotations

from typing import Any

from img2nl.features import (
    analyze_colors,
    analyze_dynamics,
    analyze_edges,
    analyze_fingerprint,
    analyze_noise,
    analyze_objects,
    analyze_patterns,
    analyze_semantic,
    analyze_special_hits,
    classify_scene,
    compare_fingerprints,
)
from img2nl.plan import ExecutionPlan, _ALL_BASE_LAYERS

_LAYER_STUBS: dict[str, dict[str, Any]] = {
    "dynamics": {"high_contrast": False, "available": False},
    "noise": {"is_flat": False, "available": False},
    "objects": {"has_large_objects": False, "available": False},
    "patterns": {"has_regular_pattern": False, "available": False},
    "edges": {"available": False, "text_likelihood": False, "edge_density": 0.0},
    "fingerprint": {},
}

_EMPTY_SPECIAL_HITS = {
    "barcodes": {"has_codes": False, "codes": []},
    "ocr": {"has_text": False, "text_preview": ""},
    "has_qr": False,
    "has_text": False,
}


def _run_layer(name: str, im, features: dict[str, Any]) -> dict[str, Any]:
    runners = {
        "colors": lambda: analyze_colors(im),
        "dynamics": lambda: analyze_dynamics(im),
        "noise": lambda: analyze_noise(im),
        "objects": lambda: analyze_objects(im),
        "patterns": lambda: analyze_patterns(im),
        "edges": lambda: analyze_edges(im),
        "fingerprint": lambda: analyze_fingerprint(im),
    }
    return runners[name]()


def extract_base_features(
    im,
    *,
    plan: ExecutionPlan | None = None,
    reference_fingerprint: dict | None = None,
    existing: dict[str, Any] | None = None,
) -> dict[str, Any]:
    layers = plan.base_layers if plan else _ALL_BASE_LAYERS
    features: dict[str, Any] = dict(existing or {})

    for layer in _ALL_BASE_LAYERS:
        if layer not in layers:
            if layer != "colors":
                features[layer] = dict(_LAYER_STUBS[layer])
            continue
        if layer in features and layer != "colors":
            continue
        features[layer] = _run_layer(layer, im, features)

    features["colors"] = features.get("colors") or analyze_colors(im)

    if reference_fingerprint is not None:
        features["fingerprint"] = analyze_fingerprint(im)
        features["similarity"] = compare_fingerprints(
            features["fingerprint"],
            reference_fingerprint,
        )

    run_special = plan.run_special_hits if plan else True
    features["special_hits"] = (
        analyze_special_hits(im, features) if run_special else dict(_EMPTY_SPECIAL_HITS)
    )
    features["scene"] = classify_scene(features)
    return features


def apply_semantic_layer(
    im,
    features: dict[str, Any],
    *,
    enabled: bool,
) -> None:
    features["semantic_hits"] = analyze_semantic(
        im,
        features=features,
        send_to_llm=enabled,
    )
