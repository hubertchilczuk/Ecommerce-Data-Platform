"""Optional streaming ingestion (Kafka or in-process simulation)."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Iterable

import click


def stream_from_file(path: str | Path, delay: float = 0.01) -> Iterable[dict]:
    """Yield events from a JSONL file with a small delay to simulate a stream."""
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)
            time.sleep(delay)


@click.command()
@click.option("--source", default="data/raw/events.jsonl", show_default=True)
@click.option("--delay", default=0.01, show_default=True)
def main(source: str, delay: float) -> None:
    for ev in stream_from_file(source, delay):
        click.echo(ev["event_id"])


if __name__ == "__main__":
    main()
