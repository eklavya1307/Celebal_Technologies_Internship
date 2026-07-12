-- 1. Total revenue per category
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 2. Top 10 customers by total order value
SELECT
    c.customer_id,
    c.customer_name,
    c.customer_type,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS total_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name, c.customer_type
ORDER BY total_order_value DESC
LIMIT 10;

-- 3. Month-wise order count for the last 12 months in the dataset
WITH max_month AS (
    SELECT date(MAX(order_date), 'start of month') AS month_start FROM orders
)
SELECT
    strftime('%Y-%m', o.order_date) AS order_month,
    COUNT(*) AS order_count
FROM orders o
CROSS JOIN max_month m
WHERE date(o.order_date) >= date(m.month_start, '-11 months')
GROUP BY order_month
ORDER BY order_month;

-- 4. Customers who placed orders but never had any item delivered
SELECT DISTINCT
    c.customer_id,
    c.customer_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE NOT EXISTS (
    SELECT 1
    FROM orders delivered_order
    WHERE delivered_order.customer_id = c.customer_id
      AND delivered_order.status = 'DELIVERED'
);

-- 5. Products that were ordered but had more returns than purchases
SELECT
    p.product_id,
    p.product_name,
    SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS returned_units,
    SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS purchased_units
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
HAVING returned_units > purchased_units
ORDER BY returned_units DESC;

-- 6. Return rate per category
SELECT
    p.category,
    SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS returned_items,
    SUM(ABS(oi.quantity)) AS total_items,
    ROUND(100.0 * SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) / NULLIF(SUM(ABS(oi.quantity)), 0), 2) AS return_rate_percent
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY return_rate_percent DESC;

-- Additional Week 8 aggregation: AOV by customer segment
SELECT
    c.customer_type,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_type
ORDER BY average_order_value DESC;
