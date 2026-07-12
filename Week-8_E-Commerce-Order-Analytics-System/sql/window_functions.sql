-- 7. Running total of revenue per region, ordered by date
WITH daily_revenue AS (
    SELECT
        o.region_code,
        date(o.order_date) AS order_date,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.region_code, date(o.order_date)
)
SELECT
    region_code,
    order_date,
    ROUND(daily_revenue, 2) AS daily_revenue,
    ROUND(SUM(daily_revenue) OVER (
        PARTITION BY region_code
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total
FROM daily_revenue
ORDER BY region_code, order_date;

-- 8. Rank products by revenue within category using DENSE_RANK
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    GROUP BY p.category, p.product_id, p.product_name
)
SELECT
    category,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;

-- 9. Days between consecutive orders and average-gap risk flag
WITH order_gaps AS (
    SELECT
        customer_id,
        date(order_date) AS order_date,
        LAG(date(order_date)) OVER (PARTITION BY customer_id ORDER BY date(order_date)) AS previous_order_date
    FROM orders
    WHERE customer_id <> 0
),
gap_values AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,
        CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER) AS days_gap
    FROM order_gaps
),
avg_gaps AS (
    SELECT customer_id, AVG(days_gap) AS avg_days_gap
    FROM gap_values
    WHERE days_gap IS NOT NULL
    GROUP BY customer_id
)
SELECT
    g.customer_id,
    g.order_date,
    g.previous_order_date,
    g.days_gap,
    CASE WHEN a.avg_days_gap > 30 THEN 'At Risk' ELSE 'Active' END AS risk_flag
FROM gap_values g
LEFT JOIN avg_gaps a ON g.customer_id = a.customer_id
ORDER BY g.customer_id, g.order_date;

-- 11. Segment customers into lifetime value quartiles with NTILE
WITH customer_value AS (
    SELECT
        c.customer_id,
        ROUND(COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0), 2) AS total_value
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    WHERE c.customer_id <> 0
    GROUP BY c.customer_id
),
quartiles AS (
    SELECT
        customer_id,
        total_value,
        NTILE(4) OVER (ORDER BY total_value DESC) AS quartile
    FROM customer_value
)
SELECT
    customer_id,
    total_value,
    quartile,
    CASE quartile
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        ELSE 'Bronze'
    END AS quartile_label
FROM quartiles
ORDER BY total_value DESC;

-- 13. First and most recent purchased category per customer
WITH customer_categories AS (
    SELECT
        o.customer_id,
        p.category,
        o.order_date,
        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_purchased_category,
        LAST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS most_recent_purchased_category
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.customer_id <> 0 AND oi.quantity > 0
)
SELECT DISTINCT
    customer_id,
    first_purchased_category,
    most_recent_purchased_category,
    CASE WHEN first_purchased_category <> most_recent_purchased_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM customer_categories
ORDER BY customer_id;

-- 14. Cumulative revenue distribution by customer
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE c.customer_id <> 0
    GROUP BY c.customer_id
),
ranked AS (
    SELECT
        customer_id,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue,
        SUM(revenue) OVER () AS total_revenue
    FROM customer_revenue
)
SELECT
    customer_id,
    revenue,
    ROUND(cumulative_revenue, 2) AS cumulative_revenue,
    ROUND(100.0 * cumulative_revenue / NULLIF(total_revenue, 0), 2) AS cumulative_percent
FROM ranked
ORDER BY revenue DESC;
