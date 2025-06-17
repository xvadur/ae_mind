import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from introspective_parser import (
    Phase1LinguisticAnalyzer,
    Phase2PsychologicalIntrospector,
    Phase5Ethics,
    IntrospectiveInput,
)


def test_phase5_ethics():
    text = "Mier a ochrana deti je dôležitá."
    p1 = Phase1LinguisticAnalyzer()
    blocks = p1.run(text)
    p2 = Phase2PsychologicalIntrospector()
    insights = p2.run(blocks)
    inputs = [
        IntrospectiveInput(
            linguistic_block=b.dict(),
            psychological_block=i.dict(),
            speaker_metadata={"source": "test"},
        )
        for b, i in zip(blocks, insights)
    ]
    phase5 = Phase5Ethics()
    vecs = phase5.run(inputs)
    assert vecs
    assert vecs[0].human_rights_dignity >= 0.0
