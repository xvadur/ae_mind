"""Expert minister for emergent synthesis tasks."""

from typing import Any, Dict, List

from memory.shared_memory import SharedMemory
from agents.base_minister import BaseMinister
from utils.audit_log import write_audit_log
from ae_mind.tools import run_delphi


class MinisterOfEmergentSynthesis(BaseMinister):
    """Combine disparate data into novel insights."""

    def __init__(self, shared_memory: SharedMemory):
        # AETH: initialize with special tool references
        super().__init__("MinisterOfEmergentSynthesis", shared_memory)
        self.domain = "knowledge_fusion"
        self.special_tools = ["GNN", "BayesianCausalModel"]
        self.kpi = {"insights_generated": 0}
        self.records: List[str] = []

    def activate(self) -> None:
        # AETH: confirm minister activation
        print(f"[{self.name}] activated")

    def report_capabilities(self) -> str:
        # AETH: describe mandate and tooling
        return "Fuses knowledge into emergent insights using GNN and Bayesian models"

    def archive(self, key: str, value: Any) -> None:
        # AETH: persist synthesis output
        self.shared_memory.data.setdefault("synthesis", []).append({key: value})
        self.records.append(key)

    def process_request(self, task: str) -> str:
        # AETH: break task into subtasks and evaluate via Delphi
        subtasks = [s.strip() for s in task.split(";") if s.strip()]
        results = []
        for sub in subtasks:
            check = run_delphi(sub)
            if check.get("delphi_score", 0) < 0.5:
                continue
            context = []
            if self.premier:
                mem = self.premier.get_minister("MinisterOfMemory")
                if mem:
                    context = mem.retrieve_relevant_info(sub, top_k=1)
            result = {
                "subtask": sub,
                "delphi": check,
                "context": context,
            }
            results.append(result)
            self.archive(sub, result)
        output = str(results)
        write_audit_log({"minister": self.name, "task": task, "result": output})
        return output

    def introspect(self) -> Dict[str, Any]:
        # AETH: provide summary of archived synthesis keys
        return {"records": list(self.records)}


class AssistantOfEmergentSynthesis:
    """Assistant handling auxiliary synthesis duties."""

    def __init__(self, shared_memory: SharedMemory):
        self.name = "AssistantOfEmergentSynthesis"
        self.shared_memory = shared_memory

    def activate(self) -> None:
        # AETH: confirm assistant activation
        print(f"[{self.name}] activated")

    def log(self, message: str) -> None:
        # AETH: placeholder for advanced logging
        print(f"[AssistantOfEmergentSynthesis] {message}")
