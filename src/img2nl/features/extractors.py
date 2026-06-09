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


def extract_base_features(
    im,
    *,
    reference_fingerprint: dict | None = None,
) -> dict[str, Any]:
    features = {
        "colors": analyze_colors(im),
        "dynamics": analyze_dynamics(im),
        "noise": analyze_noise(im),
        "objects": analyze_objects(im),
        "patterns": analyze_patterns(im),
        "edges": analyze_edges(im),
        "fingerprint": analyze_fingerprint(im),
    }
    features["scene"] = classify_scene(features)
    features["special_hits"] = analyze_special_hits(im, features)
    if reference_fingerprint:
        features["similarity"] = compare_fingerprints(
            features["fingerprint"],
            reference_fingerprint,
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
