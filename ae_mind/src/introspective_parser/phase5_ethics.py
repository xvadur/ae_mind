"""Phase 5 – Sovereign Ethical Introspector."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml

from .rule_based_scanner import RuleBasedScanner
from .ethical_vector_model import EthicalVectorModel
from .coherence_tracker import CoherenceTracker
from .models import EthicalVectorBlock, IntrospectiveInput


class Phase5Ethics:
    """Orchestrate ethical analysis producing EthicalVectorBlock."""

    def __init__(self, config_path: Path | None = None) -> None:
        # AETH: načítanie konfigurácie pre etický modul
        self.config_path = config_path or Path(__file__).with_name("phase5_config.yaml")
        try:
            self.config = yaml.safe_load(self.config_path.read_text(encoding="utf-8"))
        except Exception as exc:  # pragma: no cover - config optional
            logging.warning("Failed to load config: %s", exc)
            self.config = {}
        self.scanner = RuleBasedScanner(self.config_path)
        self.model = EthicalVectorModel()
        self.tracker = CoherenceTracker()

    def analyze(self, inputs: List[IntrospectiveInput]) -> List[EthicalVectorBlock]:
        results: List[EthicalVectorBlock] = []
        for inp in inputs:
            text = inp.linguistic_block.get("sentence", "")
            if isinstance(text, dict):
                text = text.get("text", "")
            lex_counts = self.scanner.scan(text)
            vec = self.model.vectorize(text)
            coherence = self.tracker.update(vec)
            results.append(
                EthicalVectorBlock(
                    human_rights_dignity=vec.get("human_rights_dignity", 0.0),
                    environmental_sustainability=vec.get("environmental_sustainability", 0.0),
                    diversity_inclusivity=vec.get("diversity_inclusivity", 0.0),
                    peaceful_just_societies=vec.get("peaceful_just_societies", 0.0),
                    algorithmic_fairness=vec.get("algorithmic_fairness", 0.0),
                    narrative_responsibility=vec.get("narrative_responsibility", 0.0),
                    children_digital_protection=vec.get("children_digital_protection", 0.0),
                    strategic_vectors=self.model.topics(text),
                    ideological_shifts=lex_counts,
                    narrative_coherence_score=coherence,
                    provenance={
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": inp.speaker_metadata.get("source", "unknown"),
                    },
                )
            )
        return results

    def run(self, inputs: List[IntrospectiveInput]) -> List[EthicalVectorBlock]:
        try:
            return self.analyze(inputs)
        except Exception as exc:  # pragma: no cover - safety
            logging.exception("Ethics phase failed: %s", exc)
            return []
