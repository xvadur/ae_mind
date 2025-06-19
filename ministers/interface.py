"""Interface ministry responsible for user interactions."""

from typing import Any, Dict

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister


class MinisterOfInterface(BaseMinister):
    """Manage presentation and user-facing outputs."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: initialize interface resources
        super().__init__("MinisterOfInterface", shared_memory)
        self.records: Dict[str, Any] = {}

    def activate(self) -> None:
        """Activate interface routines."""
        # AETH: confirm UI channels ready
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        """Describe interface responsibilities."""
        # AETH: provide summary for audit
        return "Handles UI layout and presentation of outputs"

    def archive(self, key: str, value: Any) -> None:
        """Archive interface artifact."""
        # AETH: track rendered elements in shared memory
        self.shared_memory.data[key] = value
        self.records[key] = value

    def process_request(self, data: str) -> str:
        """Process interface request."""
        # AETH: track recurring requests and prepare memory context
        feedback = self._register_task(data)
        query = None
        if "query:" in data:
            query = data.split("query:", 1)[1].strip()

        context = []
        if self.premier:
            memory_minister = self.premier.get_minister("MinisterOfMemory")
            if "memory minister" in data.lower() and memory_minister:
                context = memory_minister.retrieve_relevant_info(data, top_k=1)
            elif query and memory_minister:
                context = memory_minister.retrieve_relevant_info(query, top_k=1)

        self.archive(data, data)
        result = data
        if context:
            result += f" | context:{context}"
        if feedback:
            result += f" | poser:{feedback['critique']}"
        return result

    def introspect(self) -> Dict[str, Any]:
        """Return interface logs."""
        # AETH: show stored interface records
        return {"records": list(self.records.keys())}


class AssistantOfInterface:
    """Assistant for interface operations."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: share same memory
        self.name = "AssistantOfInterface"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        """Activate assistant."""
        # AETH: confirm readiness
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        """Log UI note."""
        # AETH: placeholder for advanced logging
        print(f"[AssistantOfInterface] {message}")
