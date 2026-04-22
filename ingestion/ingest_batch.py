"""Batch ingestion: read raw JSONL events and persist them to the bronze layer."""
from __future__ import annotations

import json
from pathlib import Path

import click

from .utils import ensure_dir, partition_path


def ingest_batch(source: str | Path, bronze_root: str | Path) -> Path:
    source = Path(source)
    if not source.exists():
        raise FileNotFoundError(source)

    out_dir = ensure_dir(partition_path(bronze_root))
    out_file = out_dir / f"{source.stem}.jsonl"

    count = 0
    with source.open("r", encoding="utf-8") as src, out_file.open("w", encoding="utf-8") as dst:
        for line in src:
            if not line.strip():
                continue
            json.loads(line)  # validate
            dst.write(line)
            count += 1

    click.echo(f"Ingested {count} records → {out_file}")
    return out_file


@click.command()
@click.option("--source", default="data/raw/events.jsonl", show_default=True)
@click.option("--bronze", default="data/lake/bronze/events", show_default=True)
def main(source: str, bronze: str) -> None:
    ingest_batch(source, bronze)


if __name__ == "__main__":
    main()
