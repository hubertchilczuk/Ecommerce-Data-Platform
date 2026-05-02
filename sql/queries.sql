-- Analytical queries.

-- Top 10 products by revenue (last 30 days).
SELECT product_id, revenue, units_sold
FROM gold.top_products
ORDER BY revenue DESC
LIMIT 10;

-- Revenue trend by category for the last 30 days.
SELECT event_date, category, revenue
FROM gold.daily_revenue_by_category
WHERE event_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY event_date, category;

-- Conversion proxy: orders per buyer per category.
SELECT category,
       SUM(orders)::FLOAT / NULLIF(SUM(buyers), 0) AS orders_per_buyer
FROM gold.daily_revenue_by_category
GROUP BY category
ORDER BY orders_per_buyer DESC;
