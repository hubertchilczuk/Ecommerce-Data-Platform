FROM apache/airflow:2.9.3-python3.11

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY --chown=airflow:airflow requirements-airflow.txt /tmp/requirements-airflow.txt
RUN pip install --no-cache-dir -r /tmp/requirements-airflow.txt || true

# Project code is mounted at runtime via docker-compose volumes.
ENV PYTHONPATH=/opt/airflow:/opt/airflow/spark_jobs
