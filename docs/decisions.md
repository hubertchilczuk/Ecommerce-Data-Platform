# Architectural Decisions

Short rationale for the main technology choices. Use the ADR style for new entries.

## ADR-001: Medallion architecture (bronze / silver / gold)

**Decision.** Organize the data lake into three layers: bronze (raw), silver
(cleaned, conformed), gold (business aggregates).

**Why.** Standard, well-understood pattern; clear contracts between stages;
reprocessing is local to the affected layer.

## ADR-002: Apache Spark for transformations

**Decision.** Use PySpark for bronze→silver and silver→gold jobs.

**Why.** Scales horizontally, mature ecosystem, first-class Parquet/Delta support,
runs the same code locally and on a cluster.

## ADR-003: Apache Airflow for orchestration

**Decision.** Schedule the pipeline with Airflow (LocalExecutor for dev).

**Why.** De-facto standard, rich operator ecosystem, mature scheduling and
backfill support; easy to swap for Dagster/Prefect later if needed.

## ADR-004: Pydantic schemas for events

**Decision.** Define event schemas in Pydantic and serialize to JSONL for the
bronze layer.

**Why.** Strong typing in Python, easy validation, low friction for the
generator and tests; JSONL is trivial to inspect.

## ADR-005: Terraform for infrastructure

**Decision.** Provision cloud infra (S3 / IAM / etc.) via Terraform.

**Why.** Declarative, reviewable, environment-parameterized, vendor-agnostic
enough for dev/prod parity.

## ADR-006: Optional streaming (Kafka)

**Decision.** Provide a simple streaming ingestion stub; treat real Kafka as
optional.

**Why.** Keeps the local stack lightweight while leaving the door open for a
true streaming path.
