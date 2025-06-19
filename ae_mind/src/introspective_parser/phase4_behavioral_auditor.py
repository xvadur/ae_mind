"""Phase 4 Behavioral Audit and Rhetorical Analysis."""

from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Dict, List

from .models import SpeakerProfile, BehavioralAuditBlock


class Phase4BehavioralAuditor:
    """Analyze speaker profiles for manipulative or rhetorical behavior."""

    def __init__(self) -> None:
        """Initialize regex patterns and heuristic scores."""
        # AETH: príprava heuristických pravidiel pre audit správania
        self.patterns = {
            "rhetorical_question": re.compile(r"\?"),
            "polarity_framing": re.compile(r"\bmy\b.*\boni\b|\boni\b.*\bmy\b", re.IGNORECASE),
            "emotional_priming": re.compile(r"strach|vina|hanba", re.IGNORECASE),
            "generalization": re.compile(r"vždy|nikdy", re.IGNORECASE),
        }

    def audit_profile(self, profile: SpeakerProfile) -> BehavioralAuditBlock:
        """Return a behavioral audit block for the given profile."""
        text = " ".join(profile.utterances)
        manip_phrases: List[str] = []
        counts: Dict[str, int] = {}
        for name, pattern in self.patterns.items():
            matches = pattern.findall(text)
            if matches:
                manip_phrases.append(name)
                counts[name] = len(matches)

        rational_score = 1.0 - (len(counts.get("emotional_priming", [])) / (len(text.split()) or 1))
        emotional_score = 1.0 - rational_score

        # AETH: jednoduchý odhad indexu zmeny naratívu na základe časového radu
        narrative_shift_index = float(len(set(p["mbti"] for p in profile.time_series.values())))

        manipulation_scores = {
            "demagogy": float(counts.get("polarity_framing", 0)),
            "populism": float(counts.get("generalization", 0)),
            "sophism": float(counts.get("rhetorical_question", 0)),
        }

        return BehavioralAuditBlock(
            speaker_id=profile.speaker_id,
            manipulative_phrases=manip_phrases,
            rational_score=rational_score,
            emotional_score=emotional_score,
            narrative_shift_index=narrative_shift_index,
            manipulation_scores=manipulation_scores,
            timestamp=datetime.utcnow(),
        )

    def persist(self, profiles: List[SpeakerProfile], path: str) -> None:
        """Save audited profiles to parquet and JSONL."""
        try:
            import pandas as pd

            records = []
            for p in profiles:
                data = p.model_dump()
                if data.get("behavioral_audit"):
                    ba = data["behavioral_audit"]
                    ba["timestamp"] = ba["timestamp"].isoformat()
                    data["behavioral_audit"] = ba
                records.append(data)
            df = pd.DataFrame(records)
            df.to_parquet(path)
            df.to_json(path.replace(".parquet", ".jsonl"), orient="records", lines=True, force_ascii=False)
        except Exception as exc:  # pragma: no cover - optional dependency
            logging.exception("Failed to persist Phase4 output: %s", exc)

    def run(self, profiles: List[SpeakerProfile], output: str | None = None) -> List[SpeakerProfile]:
        """Attach behavioral audit blocks to profiles and optionally persist."""
        for profile in profiles:
            try:
                profile.behavioral_audit = self.audit_profile(profile)
            except Exception as exc:  # pragma: no cover - safety
                logging.exception("Behavioral audit failed: %s", exc)
        if output:
            self.persist(profiles, output)
        return profiles
