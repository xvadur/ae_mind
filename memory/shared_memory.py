"""Shared memory with audit log capabilities."""


class SharedMemory:
    """Provide basic key-value store and logging."""

    def __init__(self, log_path: str = "memory/aeth_mem_0003.jsonl"):
        # AETH: initialize shared memory and log path
        self.data = {}
        self.log_path = log_path

    def load(self) -> None:
        """Placeholder for loading persisted state."""
        # AETH: in real system we would restore from disk
        print("Zdieľaná pamäť načítaná.")

    def write_log(self, entry: dict) -> None:
        """Append an entry to the audit trail."""
        # AETH: store structured event with timestamp
        from datetime import datetime
        entry["timestamp"] = datetime.utcnow().isoformat()
        with open(self.log_path, "a", encoding="utf-8") as f:
            import json
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_logs_for_agent(self, agent_name: str, limit: int = 10) -> list:
        """Return recent log entries related to an agent."""
        import json
        from pathlib import Path

        log_file = Path(self.log_path)
        if not log_file.exists():
            return []

        entries = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if (
                    entry.get("from") == agent_name
                    or entry.get("to") == agent_name
                    or entry.get("minister") == agent_name
                ):
                    entries.append(entry)
        return entries[-limit:]
