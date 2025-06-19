from __future__ import annotations

import json
from typing import Any, Dict

from memory.shared_memory import SharedMemory
from ae_mind.llm_client import generate_structured_reflection


class BaseMinister:
    """Common functionality for all ministers."""

    schema = {
        "achievements": [],
        "challenges": [],
        "learnings": [],
        "improvement_suggestions": [],
        "data_gaps": [],
    }

    def __init__(self, name: str, shared_memory: SharedMemory) -> None:
        self.name = name
        self.shared_memory = shared_memory
        # AETH: premier reference allows cross-minister collaboration
        self.premier = None
        # AETH: track how often tasks repeat for POSER feedback
        self.retry_counter: Dict[str, int] = {}

    def set_premier(self, premier: "Premier") -> None:
        """Register premier for later interactions."""
        # AETH: store premier reference for RAG retrieval and task routing
        self.premier = premier

    def _register_task(self, task: str) -> Dict[str, Any] | None:
        """Track task frequency and invoke POSER if repeated too often."""
        count = self.retry_counter.get(task, 0) + 1
        self.retry_counter[task] = count
        if count > 3:
            from ae_mind.tools import run_poser
            from utils.audit_log import write_audit_log

            feedback = run_poser(task)
            write_audit_log(
                {
                    "minister": self.name,
                    "task": task,
                    "poser_feedback": feedback,
                }
            )
            return feedback
        return None

    def reflect(self) -> Dict[str, Any]:
        """Use LLM to generate semantic reflection over recent logs."""
        # AETH: gather recent logs for this minister
        logs = self.shared_memory.get_logs_for_agent(self.name, limit=10)
        prompt = (
            f"Agent: {self.name}\n"
            "Recent activity logs:\n"
            f"{json.dumps(logs, ensure_ascii=False, indent=2)}\n"
            "Provide a short reflection in JSON matching this schema:\n"
            f"{json.dumps(self.schema, indent=2)}"
        )
        reflection = generate_structured_reflection(prompt, self.schema)

        # AETH: augment reflection with self-critique and alignment checks
        from datetime import datetime
        from ae_mind.tools import run_elk, run_poser

        reflection_text = json.dumps(reflection, ensure_ascii=False)
        poser_result = run_poser(reflection_text)
        elk_result = run_elk(reflection_text)

        return {
            "minister": self.name,
            "reflection": reflection,
            "poser_critique": poser_result.get("critique"),
            "poser_suggestions": poser_result.get("suggestions"),
            "elk_alignment_score": elk_result.get("alignment_score"),
            "elk_latent_knowledge": elk_result.get("latent_knowledge"),
            "timestamp": datetime.utcnow().isoformat(),
        }
