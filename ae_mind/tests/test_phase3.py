import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from introspective_parser import (
    Phase1LinguisticAnalyzer,
    Phase2PsychologicalIntrospector,
    Phase3SpeakerSynthesizer,
)


def test_phase3_synthesis():
    text = "Rad hovorím o plánoch. Som šťastný."
    p1 = Phase1LinguisticAnalyzer()
    blocks = p1.run(text)
    p2 = Phase2PsychologicalIntrospector()
    insights = p2.run(blocks)
    synth = Phase3SpeakerSynthesizer()
    profiles = synth.run(blocks, insights)
    assert profiles
    prof = profiles[0]
    assert prof.speaker_id == insights[0].speaker_id
    assert prof.mbti_distribution
    assert prof.emotion_trends
