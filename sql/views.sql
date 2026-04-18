-- Convenience views over the gold layer.

CREATE OR REPLACE VIEW gold.v_revenue_last_7d AS
SELECT event_date, category, revenue
FROM gold.daily_revenue_by_category
WHERE event_date >= CURRENT_DATE - INTERVAL '7 days';

CREATE OR REPLACE VIEW gold.v_top_products_top50 AS
SELECT *
FROM gold.top_products
ORDER BY revenue DESC
LIMIT 50;
