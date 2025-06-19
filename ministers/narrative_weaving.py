"""Expert minister crafting cohesive narratives."""

from typing import Any, Dict, List

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister
from utils.audit_log import write_audit_log
from ae_mind.tools import run_delphi


class MinisterOfNarrativeWeaving(BaseMinister):
    """Produce complex narratives from system data."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: load special NLP tools
        super().__init__("MinisterOfNarrativeWeaving", shared_memory)
        self.domain = "storytelling"
        self.special_tools = ["AdvancedNLP", "LLMChains"]
        self.kpi = {"narratives_created": 0}
        self.threads: List[str] = []

    def activate(self) -> None:
        # AETH: announce readiness
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        # AETH: describe storytelling skills
        return "Creates narratives using advanced NLP chains"

    def archive(self, key: str, value: Any) -> None:
        # AETH: store narrative piece
        self.shared_memory.data.setdefault("narratives", []).append({key: value})
        self.threads.append(key)

    def process_request(self, task: str) -> str:
        # AETH: break down narrative task into pieces
        pieces = [p.strip() for p in task.split(";") if p.strip()]
        story_parts = []
        for piece in pieces:
            evaluation = run_delphi(piece)
            story_part = {"piece": piece, **evaluation}
            story_parts.append(story_part)
            self.archive(piece, story_part)
        output = str(story_parts)
        write_audit_log({"minister": self.name, "task": task, "result": output})
        return output

    def introspect(self) -> Dict[str, Any]:
        # AETH: provide list of narrative threads
        return {"threads": list(self.threads)}


class AssistantOfNarrativeWeaving:
    """Assistant supporting narrative tasks."""

    def __init__(self, shared_memory: SharedMemory):
        self.name = "AssistantOfNarrativeWeaving"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        # AETH: confirm activation
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        # AETH: placeholder logging
        print(f"[AssistantOfNarrativeWeaving] {message}")
