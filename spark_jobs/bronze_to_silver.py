"""Bronze → Silver: clean & normalize raw events."""
from __future__ import annotations

import click

from .session import get_spark
from .transformations import clean_events


@click.command()
@click.option("--bronze", default="data/lake/bronze/events", show_default=True)
@click.option("--silver", default="data/lake/silver/events", show_default=True)
def main(bronze: str, silver: str) -> None:
    spark = get_spark("bronze-to-silver")
    df = spark.read.json(bronze)
    cleaned = clean_events(df)
    (
        cleaned.write
               .mode("overwrite")
               .partitionBy("event_date")
               .parquet(silver)
    )
    click.echo(f"Wrote silver dataset → {silver}")


if __name__ == "__main__":
    main()
