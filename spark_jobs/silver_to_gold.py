"""Silver → Gold: business-level aggregations."""
from __future__ import annotations

import click

from .session import get_spark
from .transformations import daily_revenue_by_category, top_products


@click.command()
@click.option("--silver", default="data/lake/silver/events", show_default=True)
@click.option("--gold", default="data/lake/gold", show_default=True)
def main(silver: str, gold: str) -> None:
    spark = get_spark("silver-to-gold")
    df = spark.read.parquet(silver)

    daily_revenue_by_category(df).write.mode("overwrite").parquet(f"{gold}/daily_revenue_by_category")
    top_products(df).write.mode("overwrite").parquet(f"{gold}/top_products")

    click.echo(f"Wrote gold datasets → {gold}")


if __name__ == "__main__":
    main()
