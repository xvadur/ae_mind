class Premier:
    def __init__(self, council, shared_memory, constitution):
        self.name = "Premier Aethero_Xvadur"
        self.council = council
        self.shared_memory = shared_memory
        self.constitution = constitution
        # AETH: queue for adaptive directives generated from reflections
        self.task_queue: list[dict] = []
        # AETH: audit log path for directive dispatching
        self.audit_log_path = "logs/audit_log.jsonl"
        for minister, _ in self.council:
            if hasattr(minister, "set_premier"):
                minister.set_premier(self)
        # AETH: track main loop cycles for audit grouping
        self.cycle_counter = 0
    def run_government(self):
        print(f"{self.name} inicializuje vládu podľa ústavy.")
        for minister, assistant in self.council:
            minister.activate()
            assistant.activate()
        print("Vláda AetheroOS je pripravená na výkon.")

    def run_reflection_cycle(self) -> None:
        """Collect reflections from all ministers and synthesize directives."""
        from datetime import datetime
        from ae_mind.llm_client import generate_structured_reflection
        from pathlib import Path
        import json

        reflections = {}
        for minister, _ in self.council:
            if hasattr(minister, "reflect"):
                reflections[minister.name] = minister.reflect()

        # AETH: aggregate challenges for system-level synthesis
        challenges = []
        for data in reflections.values():
            challenges.extend(data.get("challenges", []))

        system_schema = {
            "system_challenges": [],
            "synergies_conflicts": [],
            "premier_directives": [],
            "overall_data_gaps": [],
        }
        prompt = (
            "System reflection based on ministerial challenges:\n"
            f"{challenges}\nSummarize in JSON using schema:\n"
            f"{system_schema}"
        )
        system_reflection = generate_structured_reflection(prompt, system_schema)

        blocked = []
        priority_adjustments = []
        directives_file = Path("memory/premier_directives.jsonl")
        directives = []
        if directives_file.exists():
            for line in directives_file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)
                directives.append(d)
                statuses = d.get("status", {})
                attempts = d.get("attempts", {})
                incomplete = [m for m, st in statuses.items() if st != "completed"]
                if incomplete:
                    blocked.append({"directive_id": d.get("directive_id"), "blocked_ministers": incomplete})
                for m in statuses:
                    att = attempts.get(m, 0)
                    if statuses[m] != "completed" and att >= 3:
                        d["priority"] = max(0, d.get("priority", 1.0) - 0.2)
                        priority_adjustments.append({"directive_id": d.get("directive_id"), "minister": m, "adjustment": -0.2})
                    elif statuses[m] == "completed" and att <= 1:
                        d["priority"] = d.get("priority", 1.0) + 0.1
                        priority_adjustments.append({"directive_id": d.get("directive_id"), "minister": m, "adjustment": 0.1})

            # persist any priority updates
            directives_file.write_text("\n".join(json.dumps(d, ensure_ascii=False) for d in directives) + "\n", encoding="utf-8")

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "reflections": reflections,
            "system": system_reflection,
            "blocked_directives": blocked,
            "priority_adjustments": priority_adjustments,
        }
        with open("memory/premier_reflection_0001.jsonl", "a", encoding="utf-8") as f:
            import json
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def generate_adaptive_directives(self) -> list[dict] | None:
        """Use LLM to create new directives from the last reflection."""
        import json
        from pathlib import Path
        from ae_mind.llm_client import generate_structured_reflection

        # AETH: load last reflection entry
        path = Path("memory/premier_reflection_0001.jsonl")
        if not path.exists():
            print("No reflections found for directive generation.")
            return None
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines:
            return None
        last = json.loads(lines[-1])
        system_reflection = last.get("system", {})

        schema = {
            "directives": [
                {"target_ministers": ["MinisterOfMemory"], "task": ""}
            ]
        }
        prompt = (
            "Based on this reflection generate new directives:\n"
            f"{json.dumps(system_reflection, ensure_ascii=False, indent=2)}\n"
            "Return JSON using schema:\n"
            f"{json.dumps(schema, indent=2)}"
        )

        result = generate_structured_reflection(prompt, schema)
        directives = result.get("directives", [])

        # AETH: evaluate each directive via Delphi consequence modeling
        from ae_mind.tools import run_delphi

        from uuid import uuid4
        from datetime import datetime

        checked: list[dict] = []
        for item in directives:
            check = run_delphi(item.get("task", ""), context=system_reflection)
            score = check.get("delphi_score", 0)
            item.update(check)
            if score >= 0.5:
                item["directive_id"] = str(uuid4())
                mins = item.get("target_ministers", [])
                item["status"] = {m: "pending" for m in mins}
                item["timestamps"] = {"created": datetime.utcnow().isoformat(), "last_update": ""}
                item["priority"] = 1.0
                item["attempts"] = {m: 0 for m in mins}
                checked.append(item)

        with open("memory/premier_directives.jsonl", "a", encoding="utf-8") as f:
            for item in checked:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                self.task_queue.append(item)

        return checked

    def get_minister(self, name: str):
        """Return minister instance by class name."""
        for minister, _ in self.council:
            if minister.__class__.__name__ == name:
                return minister
        return None

    def send_task(self, target_ministry: str, task: str) -> str:
        """Send a task to a specific ministry and log the response."""
        # AETH: locate ministry by class name
        ministry = next((m for m, _ in self.council if m.__class__.__name__ == target_ministry), None)
        if not ministry:
            response = f"Ministerstvo {target_ministry} neexistuje."
        else:
            response = ministry.process_request(task)
        # AETH: log request and response
        self.shared_memory.write_log(
            {
                "type": "TASK",
                "from": self.name,
                "to": target_ministry,
                "task": task,
                "response": response,
            }
        )
        print(f"TASK pre {target_ministry}: {task} → {response}")
        return response

    def show_status(self) -> None:
        """Print status of all directives."""
        import json
        from pathlib import Path

        path = Path("memory/premier_directives.jsonl")
        if not path.exists():
            print("No directives recorded.")
            return
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            ident = d.get("directive_id")
            status = d.get("overall_status", "pending")
            print(f"{ident}: {status} -> {d.get('status')}")

    def show_queue(self) -> None:
        """Display directives sorted by priority."""
        import json
        from pathlib import Path

        path = Path("memory/premier_directives.jsonl")
        if not path.exists():
            print("No directives recorded.")
            return

        directives = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            directives.append(json.loads(line))

        directives.sort(key=lambda d: d.get("priority", 1.0), reverse=True)
        for d in directives:
            ident = d.get("directive_id")
            priority = d.get("priority", 1.0)
            status = d.get("overall_status", "pending")
            print(f"{priority:.2f} {ident}: {status} -> {d.get('status')}")

    def dispatch_directives(self, cycle_id: int) -> None:
        """Send queued directives to ministries and log progress."""
        import json
        from pathlib import Path
        from utils.audit_log import write_audit_log
        from ae_mind.tools import run_poser

        path = Path("memory/premier_directives.jsonl")
        if not path.exists():
            return

        directives = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            directives.append(json.loads(line))

        directives.sort(key=lambda d: d.get("priority", 1.0), reverse=True)

        updated: list[str] = []
        new_directives: list[dict] = []
        original_directives = list(directives)
        for directive in original_directives:
            statuses = directive.get("status", {})
            overall_changed = False
            results = directive.get("results", {})
            for minister in directive.get("target_ministers", []):
                if statuses.get(minister) == "completed":
                    continue
                statuses[minister] = "in_progress"
                response = self.send_task(minister, directive.get("task", ""))
                results[minister] = response
                statuses[minister] = "completed"
                attempts = directive.setdefault("attempts", {})
                attempts[minister] = attempts.get(minister, 0) + 1
                overall_changed = True
                poser_feedback = run_poser(response)
                write_audit_log(
                    {
                        "cycle_id": cycle_id,
                        "directive_id": directive.get("directive_id"),
                        "minister": minister,
                        "minister_result": response,
                        "poser_feedback": poser_feedback,
                    }
                )
                for suggestion in poser_feedback.get("suggestions", []):
                    from uuid import uuid4
                    from datetime import datetime
                    new_dir = {
                        "directive_id": str(uuid4()),
                        "target_ministers": [minister],
                        "task": suggestion,
                        "priority": directive.get("priority", 1.0),
                        "status": {minister: "pending"},
                        "attempts": {minister: 0},
                        "timestamps": {
                            "created": datetime.utcnow().isoformat(),
                            "last_update": "",
                        },
                    }
                    new_directives.append(new_dir)
                    write_audit_log(
                        {
                            "cycle_id": cycle_id,
                            "directive_id": new_dir["directive_id"],
                            "minister": minister,
                            "reason": "POSER_followup",
                        }
                    )
            directive["status"] = statuses
            directive["results"] = results
            if overall_changed:
                from datetime import datetime
                directive.setdefault("timestamps", {}).update(
                    {"last_update": datetime.utcnow().isoformat()}
                )
            directive["overall_status"] = (
                "completed" if all(s == "completed" for s in statuses.values()) else "in_progress"
            )
            updated.append(json.dumps(directive, ensure_ascii=False))

        for nd in new_directives:
            updated.append(json.dumps(nd, ensure_ascii=False))

        updated_data = [json.loads(u) for u in updated]
        updated_data.sort(key=lambda d: d.get("priority", 1.0), reverse=True)
        path.write_text(
            "\n".join(json.dumps(d, ensure_ascii=False) for d in updated_data) + "\n",
            encoding="utf-8",
        )

    def main_loop(self, cycles: int = 1, wait_seconds: int = 0) -> None:
        """Run continuous dispatch and reflection cycles."""
        import time

        for _ in range(cycles):
            self.cycle_counter += 1
            self.dispatch_directives(self.cycle_counter)
            self.run_reflection_cycle()
            self.generate_adaptive_directives()
            if wait_seconds:
                time.sleep(wait_seconds)
