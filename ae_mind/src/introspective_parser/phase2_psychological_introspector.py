"""Phase2_PsychologicalIntrospector – advanced psychological analysis."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .models import LinguisticBlock, PsychologicalBlock


class MBTIClassifier:
    """Heuristic MBTI classifier with optional transformers backend."""

    def __init__(self, model_name: str = "gerulata/slovakbert") -> None:
        self.model_name = model_name
        self.version = model_name
        try:  # pragma: no cover - heavy dependency
            from transformers import pipeline

            self.pipe = pipeline("feature-extraction", model=model_name)
        except Exception:  # pragma: no cover - fallback
            logging.warning("transformers unavailable; using heuristics")
            self.pipe = None
            self.version = "heuristic-0.1"

    def predict(self, text: str) -> tuple[str, float, Dict[str, float]]:
        """Return MBTI type with simple heuristics."""
        if self.pipe:  # pragma: no cover - not tested without transformers
            _ = self.pipe(text[:512])
            # AETH: placeholder using embedding size as random heuristic
            score = float(len(text) % 100) / 100
            mbti = "INTJ" if score > 0.5 else "ENFP"
            dims = {"IE": 0.8 if "I" in mbti else 0.2, "NS": 0.5, "FT": 0.6, "PJ": 0.4}
            return mbti, score, dims
        # heuristic fallback
        mbti = "I" if " ja " in text.lower() else "E"
        mbti += "N" if "mysl" in text.lower() else "S"
        mbti += "F" if "cít" in text.lower() else "T"
        mbti += "J" if "plán" in text.lower() else "P"
        dims = {
            "IE": 1.0 if mbti[0] == "I" else 0.0,
            "NS": 1.0 if mbti[1] == "N" else 0.0,
            "FT": 1.0 if mbti[2] == "F" else 0.0,
            "PJ": 1.0 if mbti[3] == "J" else 0.0,
        }
        return mbti, 0.5, dims


class EmotionDetector:
    """Simple rule-based emotion detector."""

    def __init__(self) -> None:
        self.version = "heuristic-0.1"
        self.emotion_keywords = {
            "joy": ["rados", "šťast", "vesel"],
            "sadness": ["smútok", "zarmút"],
            "anger": ["hnev", "nahnev"],
            "fear": ["strach", "obava"],
            "disgust": ["nechut", "odpor"],
        }

    def predict(self, text: str) -> tuple[str, float, Dict[str, float]]:
        text_l = text.lower()
        scores: Dict[str, float] = {e: 0.0 for e in self.emotion_keywords}
        for emo, keys in self.emotion_keywords.items():
            for k in keys:
                if k in text_l:
                    scores[emo] += 1
        if all(v == 0 for v in scores.values()):
            scores["neutral"] = 1.0
        primary = max(scores, key=scores.get)
        conf = scores[primary] / (sum(scores.values()) or 1)
        return primary, conf, scores


class CSJosephGridInferencer:
    """Rule-based cognitive function estimator."""

    def __init__(self) -> None:
        self.version = "heuristic-0.1"

    def infer(self, text: str) -> tuple[str, Dict[str, float]]:
        axis = "Ti-Ne" if "prečo" in text.lower() else "Fi-Se"
        functions = {"Ti": 0.5, "Ne": 0.5} if axis == "Ti-Ne" else {"Fi": 0.5, "Se": 0.5}
        return axis, functions


class SanityChecker:
    """Validate coherence of psychological results."""

    def check(self, block: PsychologicalBlock) -> bool:
        ok = block.mbti_type and block.emotion_primary
        if not ok:
            logging.error("Invalid psychological block: %s", block)
        return bool(ok)


class Phase2PsychologicalIntrospector:
    """Analyze linguistic blocks to infer psychological attributes."""

    def __init__(self) -> None:
        self.mbti = MBTIClassifier()
        self.emotions = EmotionDetector()
        self.csj = CSJosephGridInferencer()
        self.checker = SanityChecker()

    def analyze(self, blocks: List[LinguisticBlock]) -> List[PsychologicalBlock]:
        results: List[PsychologicalBlock] = []
        for block in blocks:
            text = block.sentence.text
            mbti_t, mbti_c, mbti_dims = self.mbti.predict(text)
            emo_p, emo_c, emo_scores = self.emotions.predict(text)
            axis, funcs = self.csj.infer(text)
            pb = PsychologicalBlock(
                utterance_id=block.utterance_id or "0",
                speaker_id=block.speaker_id or "unknown",
                mbti_type=mbti_t,
                mbti_confidence=mbti_c,
                mbti_dimensions=mbti_dims,
                emotion_primary=emo_p,
                emotion_confidence=emo_c,
                emotion_scores=emo_scores,
                cognitive_axis=axis,
                cognitive_functions=funcs,
                timestamp=datetime.utcnow(),
                model_versions={
                    "mbti": self.mbti.version,
                    "emotion": self.emotions.version,
                    "csj": self.csj.version,
                },
            )
            if self.checker.check(pb):
                results.append(pb)
        return results

    def persist(self, blocks: List[PsychologicalBlock], path: Path) -> None:
        import pandas as pd

        records = [b.dict() for b in blocks]
        df = pd.DataFrame(records)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path)
        df.to_json(path.with_suffix(".jsonl"), orient="records", lines=True, force_ascii=False)

    def run(self, blocks: List[LinguisticBlock], output: Path | None = None) -> List[PsychologicalBlock]:
        res = self.analyze(blocks)
        if output:
            self.persist(res, output)
        return res


if __name__ == "__main__":  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description="Run psychological introspector")
    parser.add_argument("input", type=Path, help="Input text file")
    parser.add_argument("--out", type=Path, required=True, help="Output parquet file")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    phase1 = LinguisticBlock(
        sentence=None,  # type: ignore
        tokens=[],
        lemmas=[],
        pos_tags=[],
        dependencies=[],
    )
    analyzer = Phase2PsychologicalIntrospector()
    analyzer.run([phase1], args.out)

