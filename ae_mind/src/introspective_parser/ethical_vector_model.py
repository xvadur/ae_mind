"""Heuristic ethical vector model."""

from __future__ import annotations

from typing import Dict, List


class EthicalVectorModel:
    """Estimate ethical orientation of text via simple heuristics."""

    def __init__(self) -> None:
        # AETH: heuristický model bez ML záťaže
        self.keywords = {
            "human_rights_dignity": ["dôstoj", "práva"],
            "environmental_sustainability": ["klíma", "udržateľ"],
            "diversity_inclusivity": ["inkluz", "rozmanit"],
            "peaceful_just_societies": ["mier", "spravodliv"],
            "algorithmic_fairness": ["fair", "rovnos"],
            "narrative_responsibility": ["transparent", "zodpoved"],
            "children_digital_protection": ["deti", "ochrana"],
        }

    def vectorize(self, text: str) -> Dict[str, float]:
        text_l = text.lower()
        vec: Dict[str, float] = {}
        for name, keys in self.keywords.items():
            vec[name] = float(sum(1 for k in keys if k in text_l)) / (len(keys) or 1)
        return vec

    def topics(self, text: str) -> List[str]:
        """Return rough thematic tags."""
        tags: List[str] = []
        if "vzdel" in text.lower():
            tags.append("education")
        if "zdrav" in text.lower():
            tags.append("health")
        return tags
