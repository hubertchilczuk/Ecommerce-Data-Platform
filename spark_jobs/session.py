"""Spark session factory."""
from __future__ import annotations

from pyspark.sql import SparkSession


def get_spark(app_name: str = "ecommerce-data-platform", master: str | None = None) -> SparkSession:
    builder = SparkSession.builder.appName(app_name)
    if master:
        builder = builder.master(master)
    builder = (
        builder
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.sql.shuffle.partitions", "8")
    )
    return builder.getOrCreate()
