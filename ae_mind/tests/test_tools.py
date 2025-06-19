from ae_mind.tools import run_delphi, run_elk, run_poser


def test_run_delphi():
    result = run_delphi("test action", {"a": 1})
    assert "delphi_score" in result
    assert "delphi_explanation" in result


def test_run_elk():
    result = run_elk("reflection text")
    assert "alignment_score" in result
    assert "latent_knowledge" in result


def test_run_poser():
    result = run_poser("reflection text")
    assert "critique" in result
    assert "suggestions" in result
