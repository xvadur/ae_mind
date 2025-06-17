"""Rule-based lexical scanner for ethical cues."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

import yaml


class RuleBasedScanner:
    """Detect value-laden lexemes using YAML lexicons."""

    def __init__(self, lexicon_path: Path | None = None) -> None:
        # AETH: načítanie lexikónov z konfigurácie
        self.lexicon_path = lexicon_path or Path(__file__).with_name("phase5_config.yaml")
        try:
            data = yaml.safe_load(self.lexicon_path.read_text(encoding="utf-8"))
            self.lexicons: Dict[str, List[str]] = data.get("lexicons", {})  # type: ignore
        except Exception as exc:  # pragma: no cover - optional file
            logging.warning("Failed to load lexicons: %s", exc)
            self.lexicons = {}

    def scan(self, text: str) -> Dict[str, int]:
        """Return counts of lexicon matches in the text."""
        text_l = text.lower()
        results: Dict[str, int] = {}
        for tag, words in self.lexicons.items():
            results[tag] = sum(1 for w in words if w in text_l)
        return results
