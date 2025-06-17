"""Exporter module for introspective parser results."""

from typing import List
from datetime import datetime
import json
import logging
import yaml
from .models import LinguisticBlock, PsychologicalBlock, SpeakerProfile


class Exporter:
    """Export analysis results to various formats."""

    def __init__(self) -> None:
        """Prepare exporter configuration."""
        # AETH: zatiaľ bez konfigurácie, budú pridané cesty a šablóny
        pass

    def to_yaml(self, blocks: List[LinguisticBlock], insights: List[PsychologicalBlock]) -> str:
        """Create YAML frontmatter string."""
        meta = {
            "generated": datetime.utcnow().isoformat(),
            "insights": [ins.dict() for ins in insights],
        }
        return yaml.safe_dump(meta, allow_unicode=True)

    def to_markdown(self, blocks: List[LinguisticBlock]) -> str:
        """Create markdown body from linguistic blocks."""
        lines = []
        for block in blocks:
            lines.append(block.sentence.text)
        return "\n".join(lines)

    def to_json(self, blocks: List[LinguisticBlock], insights: List[PsychologicalBlock]) -> str:
        """Serialize analysis to JSON string."""
        def _convert(item: dict) -> dict:
            return {
                k: (v.isoformat() if isinstance(v, datetime) else v)
                for k, v in item.items()
            }

        data = {
            "blocks": [block.model_dump() for block in blocks],
            "insights": [_convert(ins.model_dump()) for ins in insights],
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def export_all(self, blocks: List[LinguisticBlock], insights: List[PsychologicalBlock]) -> dict:
        """Return all export formats for convenience."""
        yaml_head = self.to_yaml(blocks, insights)
        md_body = self.to_markdown(blocks)
        json_body = self.to_json(blocks, insights)
        return {"yaml": yaml_head, "markdown": md_body, "json": json_body}

    def export_profiles(self, profiles: List[SpeakerProfile], path: str) -> None:
        """Persist speaker profiles to parquet and jsonl."""
        try:
            import pandas as pd

            records = []
            for p in profiles:
                data = p.model_dump()
                # AETH: ensure datetime keys in time_series are serialized
                ts = {k.isoformat(): v for k, v in data.get("time_series", {}).items()}
                data["time_series"] = ts
                if data.get("behavioral_audit"):
                    ba = data["behavioral_audit"]
                    ba["timestamp"] = ba["timestamp"].isoformat()
                    data["behavioral_audit"] = json.dumps(ba)
                data["linguistic_summary"] = json.dumps(data.get("linguistic_summary", {}))
                records.append(data)
            df = pd.DataFrame(records)
            df.to_parquet(path)
            df.to_json(path.replace(".parquet", ".jsonl"), orient="records", lines=True, force_ascii=False)
        except Exception as exc:  # pragma: no cover - optional dependency
            # AETH: log failure to persist profiles
            logging.exception("Failed to export profiles: %s", exc)
