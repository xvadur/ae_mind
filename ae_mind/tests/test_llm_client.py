import os
import sys
from pathlib import Path
from unittest.mock import patch
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ae_mind.llm_client import generate_structured_reflection


def test_generate_structured_reflection():
    os.environ["OPENAI_API_KEY"] = "test-key"
    schema = {
        "achievements": [],
        "challenges": [],
        "learnings": [],
        "improvement_suggestions": [],
        "data_gaps": [],
    }
    fake_json = json.dumps({"achievements": ["ok"], "challenges": []})
    from types import SimpleNamespace
    fake_response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=fake_json))]
    )
    with patch("openai.chat.completions.create", return_value=fake_response):
        result = generate_structured_reflection("prompt", schema)
    assert result["achievements"] == ["ok"]
    assert "challenges" in result
