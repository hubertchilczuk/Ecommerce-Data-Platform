"""Lightweight data quality checks runnable without Great Expectations."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import click


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""


def check_no_nulls(rows: Iterable[dict], columns: list[str]) -> CheckResult:
    bad = [r for r in rows if any(r.get(c) is None for c in columns)]
    return CheckResult(
        name=f"no_nulls({','.join(columns)})",
        passed=not bad,
        detail=f"{len(bad)} rows with nulls",
    )


def check_non_negative(rows: Iterable[dict], column: str) -> CheckResult:
    bad = [r for r in rows if (r.get(column) or 0) < 0]
    return CheckResult(
        name=f"non_negative({column})",
        passed=not bad,
        detail=f"{len(bad)} negative values",
    )


def check_unique(rows: Iterable[dict], column: str) -> CheckResult:
    seen: set = set()
    dupes = 0
    for r in rows:
        v = r.get(column)
        if v in seen:
            dupes += 1
        else:
            seen.add(v)
    return CheckResult(
        name=f"unique({column})",
        passed=dupes == 0,
        detail=f"{dupes} duplicates",
    )


@click.command()
def main() -> None:
    click.echo("Data quality checks placeholder. Wire to your bronze/silver/gold datasets.")


if __name__ == "__main__":
    main()
