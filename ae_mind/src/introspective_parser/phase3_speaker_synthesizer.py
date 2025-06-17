"""Phase 3 SpeakerProfile synthesis and longitudinal analysis."""

from __future__ import annotations

import logging
from collections import defaultdict, Counter
from datetime import datetime
from typing import Any, Dict, List

from .models import LinguisticBlock, PsychologicalBlock, SpeakerProfile


class Phase3SpeakerSynthesizer:
    """Combine Phase1 and Phase2 outputs into speaker profiles."""

    def __init__(self) -> None:
        """Initialize the synthesizer."""
        # AETH: základná príprava na agregáciu profilov
        pass

    def synthesize(
        self, linguistic: List[LinguisticBlock], psychological: List[PsychologicalBlock]
    ) -> List[SpeakerProfile]:
        """Return speaker profiles aggregated from blocks."""
        profiles: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "utterances": [],
            "mbti_distribution": Counter(),
            "emotion_trends": defaultdict(list),
            "dominant_cognitive_functions": defaultdict(float),
            "time_series": {},
            "linguistic_summary": {},
            "psychological_blocks": [],
            "linguistic_blocks": [],
        })

        ling_map = {bl.utterance_id: bl for bl in linguistic}
        for pb in psychological:
            pid = pb.speaker_id
            p = profiles[pid]
            p["psychological_blocks"].append(pb)
            lb = ling_map.get(pb.utterance_id)
            if lb:
                p["linguistic_blocks"].append(lb)
                p["utterances"].append(lb.sentence.text)
            p["mbti_distribution"][pb.mbti_type] += 1
            p["emotion_trends"][pb.emotion_primary].append(pb.emotion_confidence)
            for func, score in pb.cognitive_functions.items():
                p["dominant_cognitive_functions"][func] += score
            p["time_series"][pb.timestamp] = {"mbti": pb.mbti_type, "emotion": pb.emotion_primary}

        results = []
        for spk, data in profiles.items():
            profile = SpeakerProfile(
                speaker_id=spk,
                utterances=data["utterances"],
                mbti_distribution=dict(data["mbti_distribution"]),
                emotion_trends={k: list(v) for k, v in data["emotion_trends"].items()},
                dominant_cognitive_functions=dict(data["dominant_cognitive_functions"]),
                time_series=data["time_series"],
                linguistic_summary=data["linguistic_summary"],
                psychological_blocks=data["psychological_blocks"],
                linguistic_blocks=data["linguistic_blocks"],
            )
            results.append(profile)
        return results

    def persist(self, profiles: List[SpeakerProfile], path: str) -> None:
        """Save profiles to parquet and jsonl."""
        try:
            import pandas as pd

            records = [p.__dict__ for p in profiles]
            df = pd.DataFrame(records)
            df.to_parquet(path)
            df.to_json(path.replace(".parquet", ".jsonl"), orient="records", lines=True, force_ascii=False)
        except Exception as exc:  # pragma: no cover - optional
            logging.exception("Failed to persist profiles: %s", exc)

    def run(
        self,
        linguistic: List[LinguisticBlock],
        psychological: List[PsychologicalBlock],
        output: str | None = None,
    ) -> List[SpeakerProfile]:
        """Public entry point."""
        profiles = self.synthesize(linguistic, psychological)
        if output:
            self.persist(profiles, output)
        return profiles
