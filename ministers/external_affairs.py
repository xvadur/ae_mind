"""External Affairs ministry connects AetheroOS to the outside world."""

from typing import Any, Dict

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister


class MinisterOfExternalAffairs(BaseMinister):
    """Manage external API interactions and data."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: initialize external communication resources
        super().__init__("MinisterOfExternalAffairs", shared_memory)
        self.records: Dict[str, Any] = {}

    def activate(self) -> None:
        """Activate external affairs."""
        # AETH: confirm ability to reach external services
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        """Describe external integration roles."""
        # AETH: provide mandate summary
        return "Handles API integration and external data access"

    def archive(self, key: str, value: Any) -> None:
        """Archive data fetched from external sources."""
        # AETH: store external data for future reference
        self.shared_memory.data[key] = value
        self.records[key] = value

    def process_request(self, endpoint: str) -> str:
        """Process request to external endpoint."""
        # AETH: track repeated endpoint calls and fetch memory context
        feedback = self._register_task(endpoint)
        query = None
        if "query:" in endpoint:
            query = endpoint.split("query:", 1)[1].strip()

        context = []
        if self.premier:
            memory_minister = self.premier.get_minister("MinisterOfMemory")
            if "memory minister" in endpoint.lower() and memory_minister:
                context = memory_minister.retrieve_relevant_info(endpoint, top_k=1)
            elif query and memory_minister:
                context = memory_minister.retrieve_relevant_info(query, top_k=1)

        self.archive(endpoint, f"fetched:{endpoint}")
        result = f"fetched:{endpoint}"
        if context:
            result += f" | context:{context}"
        if feedback:
            result += f" | poser:{feedback['critique']}"
        return result

    def introspect(self) -> Dict[str, Any]:
        """Return records of external interactions."""
        # AETH: list archived external calls
        return {"endpoints": list(self.records.keys())}


class AssistantOfExternalAffairs:
    """Assistant facilitating external affairs."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: share external resource memory
        self.name = "AssistantOfExternalAffairs"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        """Activate assistant."""
        # AETH: confirm readiness to support external operations
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        """Log external note."""
        # AETH: placeholder for advanced logging
        print(f"[AssistantOfExternalAffairs] {message}")
