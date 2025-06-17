import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from introspective_parser import (
    Phase1LinguisticAnalyzer,
    Phase2PsychologicalIntrospector,
    Phase3SpeakerSynthesizer,
    Exporter,
    ParserRunner,
)


def test_phase1_basic():
    analyzer = Phase1LinguisticAnalyzer()
    blocks = analyzer.run("Šťastný deň")
    assert blocks
    assert analyzer.validate_linguistic_output(blocks)
    assert blocks[0].utterance_id == "0"


def test_phase2_basic():
    analyzer = Phase1LinguisticAnalyzer()
    blocks = analyzer.run("I am happy")
    inspector = Phase2PsychologicalIntrospector()
    insights = inspector.run(blocks)
    assert insights
    assert insights[0].emotion_primary in ("joy", "neutral")


def test_exporter():
    analyzer = Phase1LinguisticAnalyzer()
    blocks = analyzer.run("Hello world")
    inspector = Phase2PsychologicalIntrospector()
    insights = inspector.run(blocks)
    exporter = Exporter()
    data = exporter.export_all(blocks, insights)
    assert "yaml" in data and "markdown" in data and "json" in data


def test_phase3_synthesizer():
    p1 = Phase1LinguisticAnalyzer()
    blocks = p1.run("Som rád. Je to dobré.")
    p2 = Phase2PsychologicalIntrospector()
    insights = p2.run(blocks)
    p3 = Phase3SpeakerSynthesizer()
    profiles = p3.run(blocks, insights)
    assert profiles


def test_runner():
    runner = ParserRunner()
    result = runner.run("We are happy")
    assert result["linguistic"]
    assert result["psychological"]
    assert result["profiles"]
