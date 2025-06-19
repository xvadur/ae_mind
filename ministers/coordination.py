"""Coordination ministry orchestrates tasks among agents."""

from typing import Any, Dict, List

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister


class MinisterOfCoordination(BaseMinister):
    """Schedule and delegate tasks."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: keep shared memory for task tracking
        super().__init__("MinisterOfCoordination", shared_memory)
        self.tasks: List[str] = []

    def activate(self) -> None:
        """Activate coordination procedures."""
        # AETH: announce readiness to manage workflows
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        """Describe coordination mandate."""
        # AETH: return capabilities for auditing
        return "Delegates and schedules tasks for all ministries"

    def archive(self, task: str) -> None:
        """Archive a completed task."""
        # AETH: store task record in shared memory
        self.shared_memory.data.setdefault("tasks", []).append(task)
        self.tasks.append(task)

    def process_request(self, task: str) -> str:
        """Register new task."""
        # AETH: detect repeated tasks and query for cross-minister context
        feedback = self._register_task(task)
        query = None
        if "query:" in task:
            query = task.split("query:", 1)[1].strip()

        context = []
        if self.premier:
            memory_minister = self.premier.get_minister("MinisterOfMemory")
            if "memory minister" in task.lower() and memory_minister:
                context = memory_minister.retrieve_relevant_info(task, top_k=1)
            elif query and memory_minister:
                context = memory_minister.retrieve_relevant_info(query, top_k=1)

        self.archive(task)
        result = f"Task '{task}' scheduled"
        if context:
            result += f" | context:{context}"
        if feedback:
            result += f" | poser:{feedback['critique']}"
        return result

    def introspect(self) -> Dict[str, Any]:
        """Inspect scheduled tasks."""
        # AETH: provide list of coordinated tasks
        return {"tasks": list(self.tasks)}


class AssistantOfCoordination:
    """Assistant handling auxiliary coordination operations."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: rely on same shared memory
        self.name = "AssistantOfCoordination"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        """Activate assistant."""
        # AETH: confirm activation state
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        """Log coordination note."""
        # AETH: placeholder for advanced logging
        print(f"[AssistantOfCoordination] {message}")
