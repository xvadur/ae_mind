"""Phase 1 linguistic analysis for Slovak texts."""

import logging
from pathlib import Path
from typing import Iterable, List, Optional

try:
    import spacy
except Exception:  # pragma: no cover - spaCy may be absent
    spacy = None

import pandas as pd

from .models import LinguisticBlock, Sentence, Token


class Phase1LinguisticAnalyzer:
    """Process text with spaCy to extract linguistic information."""

    def __init__(
        self,
        model: str = "sk_core_news_sm",
        chunk_size: int = 10000,
        batch_size: int = 50,
        n_process: int = 1,
        cache_db: Optional[str] = None,
    ) -> None:
        """Initialize spaCy pipeline."""
        # AETH: konfigurácia chunkingu a paralelizácie
        self.chunk_size = chunk_size
        self.batch_size = batch_size
        self.n_process = n_process
        self.model_name = model
        self.cache_db = cache_db
        if spacy:
            try:
                self.nlp = spacy.load(model, disable=["ner"])
            except Exception:  # pragma: no cover - model may be missing
                logging.warning(
                    "spaCy model '%s' not found, falling back to blank 'sk'",
                    model,
                )
                self.nlp = spacy.blank("sk")
                self.nlp.add_pipe("sentencizer")
        else:  # pragma: no cover - spaCy missing entirely
            self.nlp = None

        self.db = None
        if cache_db:
            try:
                import duckdb  # type: ignore

                # AETH: lokálne cacheovanie výsledkov v DuckDB
                self.db = duckdb.connect(cache_db)
                self.db.execute(
                    "CREATE TABLE IF NOT EXISTS linguistic (speaker_id VARCHAR, utterance_id VARCHAR, sentence VARCHAR, lemmas LIST<VARCHAR>, pos_tags LIST<VARCHAR>, dependencies LIST<VARCHAR>)"
                )
            except Exception:  # pragma: no cover - optional dependency
                logging.warning("DuckDB unavailable; caching disabled")

    def _iter_texts(self, text: str) -> Iterable[str]:
        """Yield text chunks for processing."""
        for i in range(0, len(text), self.chunk_size):
            yield text[i : i + self.chunk_size]

    def analyze(self, text: str) -> List[LinguisticBlock]:
        """Return linguistic blocks for the provided text."""
        blocks: List[LinguisticBlock] = []
        if not self.nlp:
            logging.error("spaCy unavailable; using naive tokenizer")
            tokens = text.split()
            tok_objs = [Token(text=t) for t in tokens]
            blocks.append(
                LinguisticBlock(
                    sentence=Sentence(text=text, tokens=tok_objs),
                    tokens=tokens,
                    lemmas=tokens,
                    pos_tags=[],
                    dependencies=[],
                    utterance_id="0",
                )
            )
            return blocks

        try:
            utterance_count = 0
            for doc in self.nlp.pipe(
                self._iter_texts(text),
                batch_size=self.batch_size,
                n_process=self.n_process,
            ):
                for sent in doc.sents:
                    tok_objs: List[Token] = []
                    tokens: List[str] = []
                    lemmas: List[str] = []
                    pos_tags: List[str] = []
                    deps: List[str] = []
                    for tok in sent:
                        if tok.is_alpha:
                            tokens.append(tok.text)
                            lemmas.append(tok.lemma_)
                            pos_tags.append(tok.pos_)
                            deps.append(tok.dep_)
                            tok_objs.append(
                                Token(text=tok.text, lemma=tok.lemma_, pos=tok.pos_, dep=tok.dep_)
                            )
                    blocks.append(
                        LinguisticBlock(
                            sentence=Sentence(text=sent.text, tokens=tok_objs),
                            tokens=tokens,
                            lemmas=lemmas,
                            pos_tags=pos_tags,
                            dependencies=deps,
                            utterance_id=str(utterance_count),
                        )
                    )
                    utterance_count += 1
        except Exception as exc:  # pragma: no cover - runtime errors
            logging.exception("Linguistic analysis failed: %s", exc)
        return blocks

    def validate_linguistic_output(self, blocks: List[LinguisticBlock]) -> bool:
        """Ensure token arrays have consistent lengths and sample validity."""
        import random

        ok = True
        for block in blocks:
            n = len(block.tokens)
            if block.pos_tags and block.dependencies:
                if not (n == len(block.lemmas) == len(block.pos_tags) == len(block.dependencies)):
                    logging.error("Inconsistent token lengths in sentence: %s", block.sentence.text)
                    ok = False

        sample = random.choice(blocks) if blocks else None
        if sample:
            # AETH: rýchly výber náhodnej vzorky pre kontrolu integrity
            logging.debug("Sanity sample: %s", sample.sentence.text)

        return ok

    def persist(self, blocks: List[LinguisticBlock], path: Path) -> None:
        """Save linguistic blocks to parquet and JSONL."""
        records = []
        for bl in blocks:
            records.append(
                {
                    "speaker_id": bl.speaker_id,
                    "utterance_id": bl.utterance_id,
                    "sentence": bl.sentence.text,
                    "lemmas": bl.lemmas,
                    "pos_tags": bl.pos_tags,
                    "dependencies": bl.dependencies,
                }
            )

        df = pd.DataFrame(records)
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(path)
        json_path = path.with_suffix(".jsonl")
        df.to_json(json_path, orient="records", lines=True, force_ascii=False)

        if self.db:
            try:
                self.db.execute("INSERT INTO linguistic SELECT * FROM df")
            except Exception as exc:  # pragma: no cover - caching optional
                logging.warning("Failed to cache to DB: %s", exc)

    def run(self, text: str, output: Path | None = None) -> List[LinguisticBlock]:
        """Public entry point executing analysis and persisting result."""
        blocks = self.analyze(text)
        if output:
            self.persist(blocks, output)
        return blocks


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run linguistic analysis phase")
    parser.add_argument("--input", required=True, help="Input text file")
    parser.add_argument("--output", required=True, help="Output parquet file")
    args = parser.parse_args()

    content = Path(args.input).read_text(encoding="utf-8")
    analyzer = Phase1LinguisticAnalyzer()
    blocks = analyzer.run(content, Path(args.output))
    if analyzer.validate_linguistic_output(blocks):
        logging.info("Phase1 completed successfully")


if __name__ == "__main__":  # pragma: no cover
    main()

