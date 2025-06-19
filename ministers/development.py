"""Development ministry handling code operations."""

from typing import Any, Dict, List

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister


class MinisterOfDevelopment(BaseMinister):
    """Manage coding and analysis tasks."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: initialize with access to shared memory for code history
        super().__init__("MinisterOfDevelopment", shared_memory)
        self.changes: List[str] = []

    def activate(self) -> None:
        """Activate development workflows."""
        # AETH: confirm readiness for code operations
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        """Describe development capabilities."""
        # AETH: introspective summary for audits
        return "Handles coding, analysis and code generation"

    def archive(self, change: str) -> None:
        """Archive development change."""
        # AETH: persist code change note
        self.shared_memory.data.setdefault("changes", []).append(change)
        self.changes.append(change)

    def process_request(self, spec: str) -> str:
        """Process development specification."""
        # AETH: track recurring tasks and break complex specs into sub steps
        feedback = self._register_task(spec)
        steps = [s.strip() for s in spec.split(";") if s.strip()]
        outputs = []
        for step in steps:
            context = []
            if self.premier:
                memory_minister = self.premier.get_minister("MinisterOfMemory")
                if memory_minister:
                    if "memory minister" in spec.lower():
                        context = memory_minister.retrieve_relevant_info(step, top_k=2)
                    else:
                        context = memory_minister.retrieve_relevant_info(step, top_k=2)
            self.archive(step)
            outputs.append(f"Processed spec: {step} | context: {context}")
        result = " | ".join(outputs)
        if feedback:
            result += f" | poser:{feedback['critique']}"
        return result

    def introspect(self) -> Dict[str, Any]:
        """Return summary of changes."""
        # AETH: provide list of archived code changes
        return {"changes": list(self.changes)}


class AssistantOfDevelopment:
    """Assistant aiding development tasks."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: mirror minister memory access
        self.name = "AssistantOfDevelopment"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        """Activate assistant."""
        # AETH: confirm activation
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        """Log development message."""
        # AETH: placeholder for advanced logging
        print(f"[AssistantOfDevelopment] {message}")
