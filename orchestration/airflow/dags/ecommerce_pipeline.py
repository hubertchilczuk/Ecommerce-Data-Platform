"""Airflow DAG for the end-to-end e-commerce pipeline."""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ecommerce_pipeline",
    description="Generate → ingest → bronze→silver→gold → quality checks",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["ecommerce", "data-platform"],
) as dag:

    generate = BashOperator(
        task_id="generate_events",
        bash_command="python -m data_generator.generator --events 50000",
    )

    ingest = BashOperator(
        task_id="ingest_batch",
        bash_command="python -m ingestion.ingest_batch",
    )

    bronze_to_silver = BashOperator(
        task_id="bronze_to_silver",
        bash_command="python -m spark_jobs.bronze_to_silver",
    )

    silver_to_gold = BashOperator(
        task_id="silver_to_gold",
        bash_command="python -m spark_jobs.silver_to_gold",
    )

    quality = BashOperator(
        task_id="data_quality",
        bash_command="python -m data_quality.checks",
    )

    generate >> ingest >> bronze_to_silver >> silver_to_gold >> quality
