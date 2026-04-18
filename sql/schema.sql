-- Analytical schema for the gold layer.

CREATE SCHEMA IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.daily_revenue_by_category (
    event_date  DATE        NOT NULL,
    category    TEXT        NOT NULL,
    revenue     NUMERIC(14,2) NOT NULL,
    buyers      BIGINT      NOT NULL,
    orders      BIGINT      NOT NULL,
    PRIMARY KEY (event_date, category)
);

CREATE TABLE IF NOT EXISTS gold.top_products (
    product_id  TEXT        PRIMARY KEY,
    revenue     NUMERIC(14,2) NOT NULL,
    units_sold  BIGINT      NOT NULL
);
