"""Communication ministry with introspective logging."""

from typing import Any, Dict

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister


class MinisterOfCommunication(BaseMinister):
    """Handle message transformation and delivery."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: maintain reference to shared memory for all communications
        super().__init__("MinisterOfCommunication", shared_memory)
        self.log: Dict[str, Any] = {}

    def activate(self) -> None:
        """Activate minister routines."""
        # AETH: confirm minister operational status
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        """Return capabilities summary."""
        # AETH: expose mandate for audits
        return "Manages formatting and delivery of messages"

    def archive(self, key: str, value: Any) -> None:
        """Archive a communication record."""
        # AETH: persist communication history
        self.shared_memory.data[key] = value
        self.log[key] = value

    def process_request(self, message: str) -> str:
        """Transform the incoming message."""
        # AETH: detect repeated tasks and query for RAG context
        feedback = self._register_task(message)
        query = None
        if "query:" in message:
            query = message.split("query:", 1)[1].strip()

        context = []
        if self.premier:
            memory_minister = self.premier.get_minister("MinisterOfMemory")
            if "memory minister" in message.lower() and memory_minister:
                context = memory_minister.retrieve_relevant_info(message, top_k=1)
            elif query and memory_minister:
                context = memory_minister.retrieve_relevant_info(query, top_k=1)

        result = message.upper()
        if context:
            result += f" | context:{context}"
        if feedback:
            result += f" | poser:{feedback['critique']}"
        self.archive(message, result)
        return result

    def introspect(self) -> Dict[str, Any]:
        """Provide introspective view of communication history."""
        # AETH: return archived keys for analysis
        return {"history": list(self.log.keys())}


class AssistantOfCommunication:
    """Assistant supporting communication tasks."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: use same shared memory reference
        self.name = "AssistantOfCommunication"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        """Signal readiness."""
        # AETH: confirm assistant activation
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        """Log assistant note."""
        # AETH: placeholder for advanced logging
        print(f"[AssistantOfCommunication] {message}")
