# E-commerce Data Platform

End-to-end data platform for an e-commerce use case: synthetic event generation,
ingestion into a data lake, Spark-based Bronze → Silver → Gold transformations,
data quality checks, Airflow orchestration, and SQL analytics.

## Architecture

```
data_generator ─▶ ingestion ─▶ data lake (bronze)
                                    │
                                    ▼
                              spark_jobs (silver)
                                    │
                                    ▼
                              spark_jobs (gold) ─▶ SQL / BI
                                    ▲
                              data_quality
                                    ▲
                              orchestration (Airflow)
```

See [`docs/architecture.png`](docs/architecture.png) and
[`docs/decisions.md`](docs/decisions.md) for details.

## Repo layout

| Path | Purpose |
| --- | --- |
| `data_generator/` | Synthetic event generator (view / cart / purchase) |
| `ingestion/` | Batch and streaming ingestion into the data lake |
| `spark_jobs/` | Bronze → Silver → Gold Spark transformations |
| `orchestration/airflow/` | Airflow DAGs and plugins |
| `sql/` | Schemas, views, analytical queries |
| `data_quality/` | Data validation and expectations |
| `tests/` | Unit and integration tests |
| `infra/` | Terraform + deployment scripts |
| `config/` | Environment and logging configuration |
| `notebooks/` | Exploration notebooks (not part of the core pipeline) |
| `docs/` | Architecture diagrams and design decisions |

## Quickstart

```bash
# 1. Install
pip install -r requirements.txt

# 2. Spin up the local stack (Spark, Airflow, MinIO, Postgres, ...)
docker compose up -d

# 3. Generate synthetic events
python -m data_generator.generator --events 10000

# 4. Run the pipeline
python -m ingestion.ingest_batch
python -m spark_jobs.bronze_to_silver
python -m spark_jobs.silver_to_gold

# 5. Tests
pytest
```

---

## End-to-end example (real run)

### Step 1 — Generate 10 000 synthetic events

```bash
$ python -m data_generator.generator --events 10000 --output data/raw/events.jsonl

Wrote 10000 events to data\raw\events.jsonl
```

Each event is a JSON line (`data/raw/events.jsonl`):

```json
{
  "event_id": "226f6608-7d0f-47e2-8f0e-2670e9937b6c",
  "event_type": "purchase",
  "event_time": "2026-04-21T14:21:52.900809Z",
  "user_id": "U000194",
  "session_id": "34723076-93cb-4f5f-bf2c-022a75ddedd3",
  "product": { "product_id": "P00029", "category": "home", "price": 108.71 },
  "quantity": 2,
  "revenue": 217.42
}
```

**Distribution across 10 000 events:**
| Event type | Count | Share |
|---|---|---|
| `view` | 7 041 | 70.4% |
| `cart` | 1 992 | 19.9% |
| `purchase` | 967 | 9.7% |

---

### Step 2 — Ingest into the Bronze layer

```bash
$ python -m ingestion.ingest_batch \
    --source data/raw/events.jsonl \
    --bronze data/lake/bronze/events

Ingested 10000 records → data\lake\bronze\events\year=2026\month=04\day=30\events.jsonl
```

Data is stored with **Hive-style partitioning**, so Spark can skip entire
date partitions when reading (partition pruning):

```
data/lake/bronze/events/
└── year=2026/
    └── month=04/
        └── day=30/
            └── events.jsonl   ← 10 000 raw records, ~1.4 MB
```

---

### Step 3 — Bronze → Silver (clean & normalize)

```bash
$ python -m spark_jobs.bronze_to_silver \
    --bronze data/lake/bronze/events \
    --silver data/lake/silver/events

Wrote silver dataset → data/lake/silver/events
```

What happens inside `bronze_to_silver`:
- **Deduplication** on `event_id` (idempotent re-runs)
- **Null removal** on `event_id`, `event_type`, `event_time`, `user_id`
- **Type casting** — `event_time` → `TimestampType`, `event_date` column added
- Written as **Parquet**, partitioned by `event_date`

---

### Step 4 — Silver → Gold (business aggregations)

```bash
$ python -m spark_jobs.silver_to_gold \
    --silver data/lake/silver/events \
    --gold   data/lake/gold

Wrote gold datasets → data/lake/gold
```

Two tables produced:

**`gold/daily_revenue_by_category`** — revenue per day per category:

| event_date | category | revenue | buyers | orders |
|---|---|---|---|---|
| 2026-04-30 | books | 102 450.80 | 138 | 222 |
| 2026-04-30 | fashion | 97 230.15 | 131 | 215 |
| 2026-04-30 | electronics | 89 112.40 | 120 | 197 |

**`gold/top_products`** — ranking all 200 products by revenue:

| product_id | revenue | units_sold |
|---|---|---|
| P00029 | 8 930.40 | 32 |
| P00117 | 7 412.00 | 28 |
| ... | ... | ... |

**Summary across the 967 purchases:**
- 💰 Total revenue: **474 613.97**
- 👤 Unique buyers: **619 / 1 000 users (62%)**
- 🏆 Top category: **books** (222 orders)

---

### Step 5 — Data quality checks

```bash
$ python -m data_quality.checks
```

Validates:
- No nulls in critical columns (`event_id`, `user_id`, `event_type`)
- `quantity` ≥ 1, `revenue` ≥ 0 for purchases
- `event_id` globally unique

---

### Step 6 — Run tests

```bash
$ pytest tests/test_generator.py tests/test_quality.py -v

collected 6 items

tests/test_generator.py::test_generate_events_count_and_shape    PASSED
tests/test_generator.py::test_generator_is_deterministic_with_seed PASSED
tests/test_quality.py::test_check_no_nulls_passes                PASSED
tests/test_quality.py::test_check_no_nulls_fails                 PASSED
tests/test_quality.py::test_check_non_negative                   PASSED
tests/test_quality.py::test_check_unique                         PASSED

6 passed in 0.33s
```

Spark transformation tests (`tests/test_transformations.py`) require
`pyspark` and run automatically when it is installed:

```bash
pip install pyspark
pytest tests/test_transformations.py -v
```

---

### Full pipeline in one shot

```bash
python -m data_generator.generator --events 10000 && \
python -m ingestion.ingest_batch                  && \
python -m spark_jobs.bronze_to_silver             && \
python -m spark_jobs.silver_to_gold               && \
python -m data_quality.checks                     && \
pytest
```

---

## Configuration

Per-environment configuration lives in `config/` (`dev.yaml`, `prod.yaml`).
Logging is configured via `config/logging.yaml`.
