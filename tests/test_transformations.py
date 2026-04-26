"""Spark transformation tests. Skipped automatically if PySpark is not available."""
from __future__ import annotations

import pytest

pyspark = pytest.importorskip("pyspark")

from pyspark.sql import SparkSession  # noqa: E402

from spark_jobs.transformations import clean_events, daily_revenue_by_category  # noqa: E402


@pytest.fixture(scope="module")
def spark():
    s = (
        SparkSession.builder
        .master("local[1]")
        .appName("tests")
        .getOrCreate()
    )
    yield s
    s.stop()


def test_clean_events_dedupes_and_drops_nulls(spark):
    data = [
        {"event_id": "1", "event_type": "view", "event_time": "2024-01-01T00:00:00Z", "user_id": "u1"},
        {"event_id": "1", "event_type": "view", "event_time": "2024-01-01T00:00:00Z", "user_id": "u1"},
        {"event_id": "2", "event_type": "view", "event_time": None, "user_id": "u2"},
    ]
    df = spark.createDataFrame(data)
    out = clean_events(df).collect()
    assert len(out) == 1
    assert out[0]["event_id"] == "1"


def test_daily_revenue_by_category(spark):
    data = [
        {
            "event_id": "1", "event_type": "purchase",
            "event_time": "2024-01-01T10:00:00Z", "user_id": "u1",
            "revenue": 100.0, "quantity": 1,
            "product": {"product_id": "P1", "category": "books", "price": 100.0},
        },
        {
            "event_id": "2", "event_type": "purchase",
            "event_time": "2024-01-01T11:00:00Z", "user_id": "u2",
            "revenue": 50.0, "quantity": 1,
            "product": {"product_id": "P2", "category": "books", "price": 50.0},
        },
    ]
    df = clean_events(spark.createDataFrame(data))
    rows = daily_revenue_by_category(df).collect()
    assert len(rows) == 1
    assert rows[0]["category"] == "books"
    assert rows[0]["revenue"] == 150.0
    assert rows[0]["buyers"] == 2
