"""Shared ingestion utilities."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def partition_path(base: str | Path, event_time: datetime | None = None) -> Path:
    """Return a Hive-style partitioned path: base/year=YYYY/month=MM/day=DD."""
    ts = event_time or datetime.now(timezone.utc)
    return Path(base) / f"year={ts.year:04d}" / f"month={ts.month:02d}" / f"day={ts.day:02d}"


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
