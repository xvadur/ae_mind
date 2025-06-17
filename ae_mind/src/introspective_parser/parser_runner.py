"""ParserRunner – Hlavný orchestrátor introspektívnej pipeline"""

from .phase1_linguistic_analyzer import Phase1LinguisticAnalyzer
from .phase2_psychological_introspector import Phase2PsychologicalIntrospector
from .phase3_speaker_synthesizer import Phase3SpeakerSynthesizer
from .phase4_behavioral_auditor import Phase4BehavioralAuditor
from .phase5_ethics import Phase5Ethics
from .asl_meta_parser import ASLMetaParser
from .models import IntrospectiveInput


class ParserRunner:
    """Execute the full introspective parsing flow."""

    def __init__(self) -> None:
        """Initialize all parser phases."""
        # AETH: inicializácia jednotlivých fáz
        self.phase1 = Phase1LinguisticAnalyzer()
        self.phase2 = Phase2PsychologicalIntrospector()
        self.phase3 = Phase3SpeakerSynthesizer()
        self.phase4 = Phase4BehavioralAuditor()
        self.phase5 = Phase5Ethics()
        self.meta_parser = ASLMetaParser()

    def run(self, text: str):
        """Run the pipeline over the given text."""
        # AETH: placeholder orchestrácia volaní jednotlivých fáz
        linguistic = self.phase1.run(text)
        psychological = self.phase2.run(linguistic)
        profiles = self.phase3.run(linguistic, psychological)
        audited = self.phase4.run(profiles)
        inputs: List[IntrospectiveInput] = []
        ling_map = {l.utterance_id: l.dict() for l in linguistic}
        for pb in psychological:
            inputs.append(
                IntrospectiveInput(
                    linguistic_block=ling_map.get(pb.utterance_id, {}),
                    psychological_block=pb.dict(),
                    speaker_metadata={"id": pb.speaker_id, "source": "pipeline"},
                )
            )
        ethics = self.phase5.run(inputs)
        meta = self.meta_parser.run(text)
        return {
            "linguistic": linguistic,
            "psychological": psychological,
            "profiles": audited,
            "ethics": ethics,
            "meta": meta,
        }

    # TODO: doplniť logovanie a spracovanie chýb podľa úrovne introspekcie
