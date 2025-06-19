from __future__ import annotations

"""Utility for writing audit logs."""

import json
from pathlib import Path
from datetime import datetime


DEFAULT_AUDIT_PATH = Path("logs/audit_log.jsonl")


def write_audit_log(entry: dict, path: Path = DEFAULT_AUDIT_PATH) -> None:
    """Append an entry to the audit log with timestamp."""
    path.parent.mkdir(parents=True, exist_ok=True)
    entry["timestamp"] = datetime.utcnow().isoformat()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
