import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from introspective_parser import (
    Phase1LinguisticAnalyzer,
    Phase2PsychologicalIntrospector,
    Phase3SpeakerSynthesizer,
    Phase4BehavioralAuditor,
)


def test_phase4_audit():
    text = "My chceme pravdu. Oni vždy klamú. Prečo nám bránia?"
    p1 = Phase1LinguisticAnalyzer()
    blocks = p1.run(text)
    p2 = Phase2PsychologicalIntrospector()
    insights = p2.run(blocks)
    synth = Phase3SpeakerSynthesizer()
    profiles = synth.run(blocks, insights)
    auditor = Phase4BehavioralAuditor()
    audited = auditor.run(profiles)
    assert audited[0].behavioral_audit is not None
    phrases = audited[0].behavioral_audit.manipulative_phrases
    assert "polarity_framing" in phrases or "rhetorical_question" in phrases
