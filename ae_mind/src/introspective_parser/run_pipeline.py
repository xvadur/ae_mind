"""CLI entry point for the introspective parser pipeline."""

import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import json

from .parser_runner import ParserRunner
from .exporter import Exporter


def load_input(path: Path) -> str:
    """Load text from HTML, JSON or plain text."""
    content = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".html":
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text(separator="\n")
    if path.suffix.lower() == ".json":
        data = json.loads(content)
        if isinstance(data, dict):
            return json.dumps(data)
        return "\n".join(map(str, data))
    return content


def main() -> None:
    parser = argparse.ArgumentParser(description="Run introspective parser pipeline")
    parser.add_argument("input", type=Path, help="Input file (HTML, JSON, TXT)")
    parser.add_argument("--out", type=Path, default=Path("output.md"), help="Output Markdown file")
    args = parser.parse_args()

    text = load_input(args.input)

    runner = ParserRunner()
    result = runner.run(text)

    exporter = Exporter()
    exported = exporter.export_all(result["linguistic"], result["psychological"])
    profiles = result.get("profiles")
    if profiles:
        profile_path = args.out.with_name(args.out.stem + "_profiles.parquet")
        exporter.export_profiles(profiles, str(profile_path))

    with args.out.open("w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(exported["yaml"])
        f.write("---\n\n")
        f.write(exported["markdown"])

    json_path = args.out.with_suffix(".json")
    with json_path.open("w", encoding="utf-8") as f:
        f.write(exported["json"])


if __name__ == "__main__":
    main()
