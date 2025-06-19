import json
import os
from typing import Dict

import openai


def generate_json_completion(prompt: str, schema: Dict) -> Dict:
    """Generic helper for LLM JSON output following schema."""
    # AETH: thin wrapper using the Agents SDK compatible API
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    model = os.getenv("OPENAI_MODEL", "gpt-4")

    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    text = response.choices[0].message.content
    data = json.loads(text)
    for key in schema:
        data.setdefault(key, schema[key])
    return data


def generate_structured_reflection(prompt: str, schema: Dict) -> Dict:
    """Call the OpenAI API with a prompt and return structured JSON.

    Parameters
    ----------
    prompt: str
        The textual prompt describing what to reflect on.
    schema: dict
        The expected JSON schema with default values.

    Returns
    -------
    dict
        Parsed JSON matching the schema.
    """
    prompt = (
        "You generate structured reflections as JSON.\n" + prompt
    )
    return generate_json_completion(prompt, schema)
