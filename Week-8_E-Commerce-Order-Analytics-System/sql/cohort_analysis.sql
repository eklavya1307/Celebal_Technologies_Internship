-- 10. Multi-level CTE: monthly revenue per customer and monthly customer tiers
WITH monthly_customer_revenue AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS revenue_month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id <> 0
    GROUP BY o.customer_id, strftime('%Y-%m', o.order_date)
),
customer_tiers AS (
    SELECT
        customer_id,
        revenue_month,
        monthly_revenue,
        CASE
            WHEN monthly_revenue > 10000 THEN 'High'
            WHEN monthly_revenue BETWEEN 5000 AND 10000 THEN 'Medium'
            ELSE 'Low'
        END AS revenue_tier
    FROM monthly_customer_revenue
)
SELECT
    revenue_month,
    revenue_tier,
    COUNT(*) AS customer_count
FROM customer_tiers
GROUP BY revenue_month, revenue_tier
ORDER BY revenue_month, revenue_tier;

-- 12. Year-over-year monthly revenue comparison
WITH monthly_revenue AS (
    SELECT
        CAST(strftime('%Y', o.order_date) AS INTEGER) AS year,
        CAST(strftime('%m', o.order_date) AS INTEGER) AS month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY year, month
)
SELECT
    current.year,
    current.month,
    ROUND(current.revenue, 2) AS revenue,
    ROUND(previous.revenue, 2) AS prev_year_revenue,
    CASE
        WHEN previous.revenue IS NULL OR previous.revenue = 0 THEN NULL
        ELSE ROUND(100.0 * (current.revenue - previous.revenue) / previous.revenue, 2)
    END AS yoy_growth_percent
FROM monthly_revenue current
LEFT JOIN monthly_revenue previous
    ON previous.year = current.year - 1
   AND previous.month = current.month
ORDER BY current.year, current.month;

-- 15. Cohort analysis: registration-month cohorts and month 0-3 retention
WITH order_months AS (
    SELECT DISTINCT
        c.customer_id,
        date(c.registration_date, 'start of month') AS cohort_month,
        date(o.order_date, 'start of month') AS activity_month
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    WHERE c.customer_id <> 0
),
cohort_activity AS (
    SELECT
        customer_id,
        strftime('%Y-%m', cohort_month) AS cohort,
        ((CAST(strftime('%Y', activity_month) AS INTEGER) - CAST(strftime('%Y', cohort_month) AS INTEGER)) * 12)
            + (CAST(strftime('%m', activity_month) AS INTEGER) - CAST(strftime('%m', cohort_month) AS INTEGER)) AS month_number
    FROM order_months
),
cohort_sizes AS (
    SELECT cohort, COUNT(DISTINCT customer_id) AS cohort_size
    FROM cohort_activity
    WHERE month_number = 0
    GROUP BY cohort
),
retention AS (
    SELECT
        cohort,
        COUNT(DISTINCT CASE WHEN month_number = 0 THEN customer_id END) AS month_0_customers,
        COUNT(DISTINCT CASE WHEN month_number = 1 THEN customer_id END) AS month_1_customers,
        COUNT(DISTINCT CASE WHEN month_number = 2 THEN customer_id END) AS month_2_customers,
        COUNT(DISTINCT CASE WHEN month_number = 3 THEN customer_id END) AS month_3_customers
    FROM cohort_activity
    WHERE month_number BETWEEN 0 AND 3
    GROUP BY cohort
)
SELECT
    r.cohort,
    COALESCE(s.cohort_size, 0) AS cohort_size,
    r.month_0_customers,
    r.month_1_customers,
    r.month_2_customers,
    r.month_3_customers,
    ROUND(100.0 * r.month_0_customers / NULLIF(s.cohort_size, 0), 2) AS month_0_retention_rate,
    ROUND(100.0 * r.month_1_customers / NULLIF(s.cohort_size, 0), 2) AS month_1_retention_rate,
    ROUND(100.0 * r.month_2_customers / NULLIF(s.cohort_size, 0), 2) AS month_2_retention_rate,
    ROUND(100.0 * r.month_3_customers / NULLIF(s.cohort_size, 0), 2) AS month_3_retention_rate
FROM retention r
LEFT JOIN cohort_sizes s ON r.cohort = s.cohort
ORDER BY r.cohort;

-- 16. Products frequently bought together, excluding duplicate A-B/B-A pairs
SELECT
    p1.product_name AS product_a,
    p2.product_name AS product_b,
    COUNT(*) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2
    ON oi1.order_id = oi2.order_id
   AND oi1.product_id < oi2.product_id
JOIN products p1 ON oi1.product_id = p1.product_id
JOIN products p2 ON oi2.product_id = p2.product_id
WHERE oi1.quantity > 0
  AND oi2.quantity > 0
GROUP BY p1.product_id, p2.product_id, p1.product_name, p2.product_name
HAVING COUNT(*) > 1
ORDER BY times_bought_together DESC, product_a, product_b
LIMIT 25;

-- Customer segmentation: purchase frequency, spend tier, and RFM-style recency
WITH metrics AS (
    SELECT
        c.customer_id,
        c.customer_name,
        COUNT(DISTINCT o.order_id) AS frequency,
        MAX(date(o.order_date)) AS last_order_date,
        ROUND(COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0), 2) AS monetary
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE c.customer_id <> 0
    GROUP BY c.customer_id, c.customer_name
),
max_date AS (
    SELECT MAX(date(order_date)) AS dataset_max_date FROM orders
)
SELECT
    m.customer_id,
    m.customer_name,
    m.frequency,
    CAST(julianday(md.dataset_max_date) - julianday(m.last_order_date) AS INTEGER) AS recency_days,
    m.monetary,
    CASE
        WHEN m.frequency <= 1 THEN 'One-Time'
        WHEN m.frequency BETWEEN 2 AND 4 THEN 'Occasional'
        ELSE 'Loyal'
    END AS frequency_segment,
    CASE
        WHEN m.monetary >= 20000 THEN 'High'
        WHEN m.monetary >= 7500 THEN 'Medium'
        ELSE 'Low'
    END AS spend_tier
FROM metrics m
CROSS JOIN max_date md
ORDER BY monetary DESC;
