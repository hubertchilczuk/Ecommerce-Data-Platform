"""Reusable DataFrame transformations."""
from __future__ import annotations

from pyspark.sql import DataFrame, functions as F


def clean_events(df: DataFrame) -> DataFrame:
    """Drop nulls in critical columns, deduplicate by event_id, normalize timestamps."""
    return (
        df.dropna(subset=["event_id", "event_type", "event_time", "user_id"])
          .dropDuplicates(["event_id"])
          .withColumn("event_time", F.to_timestamp("event_time"))
          .withColumn("event_date", F.to_date("event_time"))
    )


def daily_revenue_by_category(df: DataFrame) -> DataFrame:
    return (
        df.filter(F.col("event_type") == "purchase")
          .groupBy("event_date", F.col("product.category").alias("category"))
          .agg(
              F.sum("revenue").alias("revenue"),
              F.countDistinct("user_id").alias("buyers"),
              F.count("*").alias("orders"),
          )
    )


def top_products(df: DataFrame, limit: int = 100) -> DataFrame:
    return (
        df.filter(F.col("event_type") == "purchase")
          .groupBy(F.col("product.product_id").alias("product_id"))
          .agg(
              F.sum("revenue").alias("revenue"),
              F.sum("quantity").alias("units_sold"),
          )
          .orderBy(F.col("revenue").desc())
          .limit(limit)
    )
