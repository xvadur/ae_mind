"""Simple coherence tracker for ethical vectors."""

from __future__ import annotations

from typing import Dict, List


class CoherenceTracker:
    """Track thematic coherence across texts."""

    def __init__(self) -> None:
        self.history: List[Dict[str, float]] = []

    def update(self, vector: Dict[str, float]) -> float:
        """Return coherence score compared with history."""
        if not self.history:
            self.history.append(vector)
            return 1.0
        prev = self.history[-1]
        keys = set(vector) | set(prev)
        diff = sum(abs(vector.get(k, 0.0) - prev.get(k, 0.0)) for k in keys)
        score = 1.0 - diff / len(keys)
        self.history.append(vector)
        return max(0.0, min(1.0, score))
