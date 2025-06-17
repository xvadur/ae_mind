from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from introspective_parser.phase1_linguistic_analyzer import Phase1LinguisticAnalyzer


def test_validate_output():
    analyzer = Phase1LinguisticAnalyzer()
    blocks = analyzer.analyze("Toto je skúška.")
    assert analyzer.validate_linguistic_output(blocks)
    assert blocks[0].utterance_id == "0"

