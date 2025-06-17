from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from introspective_parser.models import IntrospectiveInput, EthicalVectorBlock


def test_models_instantiation():
    inp = IntrospectiveInput(
        linguistic_block={"text": "a"},
        psychological_block={"mbti": "INTJ"},
        speaker_metadata={"id": "s1"},
    )
    assert inp.linguistic_block["text"] == "a"

    vec = EthicalVectorBlock(
        human_rights_dignity=0.5,
        environmental_sustainability=0.5,
        diversity_inclusivity=0.5,
        peaceful_just_societies=0.5,
        algorithmic_fairness=0.5,
        narrative_responsibility=0.5,
        children_digital_protection=0.5,
        strategic_vectors=["a"],
        ideological_shifts={"x": 0.1},
        narrative_coherence_score=0.5,
        provenance={"src": "test"},
    )
    assert vec.human_rights_dignity == 0.5
