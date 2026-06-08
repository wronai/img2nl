#!/usr/bin/env python3
"""Regenerate src/img2nl/i18n/messages.json from embedded language packs."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "src/img2nl/i18n/messages.json"

LANGS = [
    "pl", "en", "de", "fr", "es", "it", "pt", "nl", "cs", "sk", "uk", "ru", "ro", "hu", "bg",
    "hr", "sr", "sl", "et", "lv", "lt", "fi", "sv", "da", "no", "is", "el", "ga", "mt", "sq",
    "mk", "be", "ca", "eu", "gl", "cy", "lb", "bs",
]

# fmt: off
PACKS: dict[str, dict[str, str]] = {
"pl": {"image_size":"Obraz {w}×{h} px.","monochrome":"Wygląda na jednokolorowy lub prawie jednokolorowy.","colors_count":"Widocznych ~{n} kolorów w próbce.","dominant_colors":"Dominują: {colors}.","brightness_range":"Jasność {b_min}–{b_max} (zakres dynamiki {dynamic}).","low_contrast":"Niski kontrast.","high_contrast":"Wysoki kontrast.","flat_surface":"Płaska powierzchnia, mało szumu.","noisy":"Widoczny szum lub drobna tekstura.","large_objects":"Wykryto {n} dużych regionów/obiektów.","no_large_objects":"Brak wyraźnych dużych obiektów.","regular_patterns":"Regularne wzorce: {hints}.","pattern_horizontal":"pasy poziome","pattern_vertical":"pasy pionowe","pattern_grid":"siatka/periodyczność","scene_empty_dark":"Scena: pusty lub ciemny ekran.","scene_ui_blocks":"Scena: układ bloków UI.","scene_ui_text":"Scena: interfejs z tekstem.","scene_dense_ui":"Scena: gęsty UI lub kod.","scene_flat_mono":"Scena: płaska powierzchnia jednokolorowa.","diag_blank":"Obraz {w}×{h} px wygląda na pusty/czarny (capture bez uprawnień?).","diag_send_llm":"Obraz {w}×{h} px, ~{unique} kolorów, jasność {b_min}–{b_max}. Warto wysłać miniaturę do LLM.","diag_grid_only":"Obraz {w}×{h} px, ~{unique} kolorów. VQL grid adopt wystarczy."},
"en": {"image_size":"Image {w}×{h} px.","monochrome":"Appears monochrome or near-monochrome.","colors_count":"About {n} distinct colors in sample.","dominant_colors":"Dominant: {colors}.","brightness_range":"Brightness {b_min}–{b_max} (dynamic range {dynamic}).","low_contrast":"Low contrast.","high_contrast":"High contrast.","flat_surface":"Flat surface, little noise.","noisy":"Visible noise or fine texture.","large_objects":"{n} large regions detected.","no_large_objects":"No clear large objects.","regular_patterns":"Regular patterns: {hints}.","pattern_horizontal":"horizontal bands","pattern_vertical":"vertical bands","pattern_grid":"grid/periodicity","scene_empty_dark":"Scene: empty or dark screen.","scene_ui_blocks":"Scene: UI block layout.","scene_ui_text":"Scene: UI with text.","scene_dense_ui":"Scene: dense UI or code.","scene_flat_mono":"Scene: flat monochrome surface.","diag_blank":"Image {w}×{h} px looks blank/black (capture without permission?).","diag_send_llm":"Image {w}×{h} px, ~{unique} colors, brightness {b_min}–{b_max}. Worth sending a thumbnail to an LLM.","diag_grid_only":"Image {w}×{h} px, ~{unique} colors. VQL grid adopt is enough."},
"de": {"image_size":"Bild {w}×{h} px.","monochrome":"Wirkt monochrom oder nahezu monochrom.","colors_count":"Etwa {n} Farben in der Stichprobe.","dominant_colors":"Dominierend: {colors}.","brightness_range":"Helligkeit {b_min}–{b_max} (Dynamikbereich {dynamic}).","low_contrast":"Niedriger Kontrast.","high_contrast":"Hoher Kontrast.","flat_surface":"Flache Fläche, wenig Rauschen.","noisy":"Sichtbares Rauschen oder feine Textur.","large_objects":"{n} große Bereiche erkannt.","no_large_objects":"Keine deutlichen großen Objekte.","regular_patterns":"Regelmäßige Muster: {hints}.","pattern_horizontal":"horizontale Streifen","pattern_vertical":"vertikale Streifen","pattern_grid":"Gitter/Periodizität","scene_empty_dark":"Szene: leerer oder dunkler Bildschirm.","scene_ui_blocks":"Szene: UI-Blocklayout.","scene_ui_text":"Szene: UI mit Text.","scene_dense_ui":"Szene: dichte UI oder Code.","scene_flat_mono":"Szene: flache monochrome Fläche.","diag_blank":"Bild {w}×{h} px wirkt leer/schwarz (Aufnahme ohne Berechtigung?).","diag_send_llm":"Bild {w}×{h} px, ~{unique} Farben, Helligkeit {b_min}–{b_max}. Miniatur an LLM senden.","diag_grid_only":"Bild {w}×{h} px, ~{unique} Farben. VQL-Grid-Adopt reicht."},
"fr": {"image_size":"Image {w}×{h} px.","monochrome":"Paraît monochrome ou presque monochrome.","colors_count":"Environ {n} couleurs distinctes dans l'échantillon.","dominant_colors":"Dominantes : {colors}.","brightness_range":"Luminosité {b_min}–{b_max} (plage dynamique {dynamic}).","low_contrast":"Faible contraste.","high_contrast":"Contraste élevé.","flat_surface":"Surface plane, peu de bruit.","noisy":"Bruit visible ou texture fine.","large_objects":"{n} grandes régions détectées.","no_large_objects":"Pas d'objets larges nets.","regular_patterns":"Motifs réguliers : {hints}.","pattern_horizontal":"bandes horizontales","pattern_vertical":"bandes verticales","pattern_grid":"grille/périodicité","scene_empty_dark":"Scène : écran vide ou sombre.","scene_ui_blocks":"Scène : disposition de blocs UI.","scene_ui_text":"Scène : interface avec texte.","scene_dense_ui":"Scène : UI dense ou code.","scene_flat_mono":"Scène : surface monochrome plane.","diag_blank":"Image {w}×{h} px semble vide/noire (capture sans permission ?).","diag_send_llm":"Image {w}×{h} px, ~{unique} couleurs, luminosité {b_min}–{b_max}. Envoyer une miniature au LLM.","diag_grid_only":"Image {w}×{h} px, ~{unique} couleurs. L'adopt VQL grid suffit."},
"es": {"image_size":"Imagen {w}×{h} px.","monochrome":"Parece monocromática o casi monocromática.","colors_count":"Unas {n} colores distintos en la muestra.","dominant_colors":"Dominantes: {colors}.","brightness_range":"Brillo {b_min}–{b_max} (rango dinámico {dynamic}).","low_contrast":"Bajo contraste.","high_contrast":"Alto contraste.","flat_surface":"Superficie plana, poco ruido.","noisy":"Ruido visible o textura fina.","large_objects":"{n} regiones grandes detectadas.","no_large_objects":"Sin objetos grandes claros.","regular_patterns":"Patrones regulares: {hints}.","pattern_horizontal":"bandas horizontales","pattern_vertical":"bandas verticales","pattern_grid":"rejilla/periodicidad","scene_empty_dark":"Escena: pantalla vacía u oscura.","scene_ui_blocks":"Escena: diseño de bloques UI.","scene_ui_text":"Escena: interfaz con texto.","scene_dense_ui":"Escena: UI densa o código.","scene_flat_mono":"Escena: superficie monocroma plana.","diag_blank":"Imagen {w}×{h} px parece vacía/negra (¿captura sin permiso?).","diag_send_llm":"Imagen {w}×{h} px, ~{unique} colores, brillo {b_min}–{b_max}. Conviene enviar miniatura al LLM.","diag_grid_only":"Imagen {w}×{h} px, ~{unique} colores. Basta adopt VQL grid."},
"it": {"image_size":"Immagine {w}×{h} px.","monochrome":"Sembra monocromatica o quasi monocromatica.","colors_count":"Circa {n} colori distinti nel campione.","dominant_colors":"Dominanti: {colors}.","brightness_range":"Luminosità {b_min}–{b_max} (gamma dinamica {dynamic}).","low_contrast":"Basso contrasto.","high_contrast":"Alto contrasto.","flat_surface":"Superficie piatta, poco rumore.","noisy":"Rumore visibile o texture fine.","large_objects":"{n} regioni grandi rilevate.","no_large_objects":"Nessun oggetto grande evidente.","regular_patterns":"Pattern regolari: {hints}.","pattern_horizontal":"bande orizzontali","pattern_vertical":"bande verticali","pattern_grid":"griglia/periodicità","scene_empty_dark":"Scena: schermo vuoto o scuro.","scene_ui_blocks":"Scena: layout a blocchi UI.","scene_ui_text":"Scena: interfaccia con testo.","scene_dense_ui":"Scena: UI densa o codice.","scene_flat_mono":"Scena: superficie monocroma piatta.","diag_blank":"Immagine {w}×{h} px sembra vuota/nera (cattura senza permesso?).","diag_send_llm":"Immagine {w}×{h} px, ~{unique} colori, luminosità {b_min}–{b_max}. Inviare miniatura all'LLM.","diag_grid_only":"Immagine {w}×{h} px, ~{unique} colori. Basta adopt VQL grid."},
}
# fmt: on

NEIGHBOR = {
    "pt": "es", "nl": "de", "cs": "sk", "sk": "cs", "uk": "ru", "ru": "uk", "ro": "it", "hu": "de",
    "bg": "ru", "hr": "bs", "sr": "hr", "sl": "hr", "et": "fi", "lv": "lt", "lt": "lv", "fi": "sv",
    "sv": "da", "da": "no", "no": "da", "is": "no", "el": "it", "ga": "en", "mt": "it", "sq": "it",
    "mk": "bg", "be": "ru", "ca": "es", "eu": "es", "gl": "pt", "cy": "ga", "lb": "de", "bs": "hr",
}

# Hand-tuned packs for additional languages (abbreviated in repo; extend in build script)
EXTRA: dict[str, dict[str, str]] = {}
# Load extended packs from messages.extra.json if present
_extra_path = Path(__file__).with_name("messages.extra.json")
if _extra_path.is_file():
    EXTRA = json.loads(_extra_path.read_text(encoding="utf-8"))

KEYS = list(PACKS["en"].keys())

for lang in LANGS:
    if lang in PACKS:
        continue
    if lang in EXTRA:
        PACKS[lang] = EXTRA[lang]
        continue
    base = PACKS.get(NEIGHBOR.get(lang, "en"), PACKS["en"]).copy()
    PACKS[lang] = base

messages: dict[str, dict[str, str]] = {key: {lang: PACKS[lang][key] for lang in LANGS} for key in KEYS}
OUT.write_text(json.dumps(messages, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote {OUT} ({len(LANGS)} langs, {len(KEYS)} keys)")
