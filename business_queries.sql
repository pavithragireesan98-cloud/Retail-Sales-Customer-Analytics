-- =============================================================================
-- RETAIL SALES & CUSTOMER ANALYTICS: BUSINESS QUERIES (SQL / MySQL)
-- Interview-Ready & Business-Oriented Analytical SQL Scripts
-- =============================================================================

USE retail_analytics_db;

-- -----------------------------------------------------------------------------
-- Q1: EXECUTIVE KPI SUMMARY (Total Revenue, Total Orders, Total Customers, AOV)
-- -----------------------------------------------------------------------------
SELECT 
    ROUND(SUM(od.line_total), 2) AS total_revenue,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT o.customer_id) AS total_customers,
    ROUND(SUM(od.line_total) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM Orders o
JOIN Order_Details od ON o.order_id = od.order_id;


-- -----------------------------------------------------------------------------
-- Q2: MONTHLY REVENUE & MONTH-OVER-MONTH (MoM) GROWTH RATE
-- Uses Window Function LAG() to calculate MoM percentage change
-- -----------------------------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(o.order_date, '%Y-%m') AS year_month,
        ROUND(SUM(od.line_total), 2) AS monthly_revenue,
        COUNT(DISTINCT o.order_id) AS monthly_orders
    FROM Orders o
    JOIN Order_Details od ON o.order_id = od.order_id
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT 
    year_month,
    monthly_revenue,
    monthly_orders,
    LAG(monthly_revenue) OVER (ORDER BY year_month) AS previous_month_revenue,
    ROUND(
        ((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY year_month)) / 
        NULLIF(LAG(monthly_revenue) OVER (ORDER BY year_month), 0)) * 100, 2
    ) AS mom_growth_percent
FROM MonthlySales
ORDER BY year_month ASC;


-- -----------------------------------------------------------------------------
-- Q3: BEST-PERFORMING PRODUCT CATEGORIES & CONTRIBUTION TO TOTAL REVENUE
-- Calculates absolute revenue and percentage share of total business sales
-- -----------------------------------------------------------------------------
SELECT 
    p.product_category,
    COUNT(DISTINCT od.order_id) AS total_orders,
    SUM(od.quantity) AS total_units_sold,
    ROUND(SUM(od.line_total), 2) AS category_revenue,
    ROUND(
        (SUM(od.line_total) / (SELECT SUM(line_total) FROM Order_Details)) * 100, 2
    ) AS revenue_contribution_percent
FROM Order_Details od
JOIN Products p ON od.product_id = p.product_id
GROUP BY p.product_category
ORDER BY category_revenue DESC;


-- -----------------------------------------------------------------------------
-- Q4: TOP 10 PRODUCTS BY REVENUE (RANKED)
-- Uses DENSE_RANK() window function to identify top revenue generators
-- -----------------------------------------------------------------------------
WITH ProductRevenue AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.product_category,
        SUM(od.quantity) AS total_quantity_sold,
        ROUND(SUM(od.line_total), 2) AS total_product_revenue,
        DENSE_RANK() OVER (ORDER BY SUM(od.line_total) DESC) AS revenue_rank
    FROM Order_Details od
    JOIN Products p ON od.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.product_category
)
SELECT revenue_rank, product_id, product_name, product_category, total_quantity_sold, total_product_revenue
FROM ProductRevenue
WHERE revenue_rank <= 10;


-- -----------------------------------------------------------------------------
-- Q5: REVENUE AND ORDERS BY CITY AND STATE
-- Geographical breakdown of sales performance
-- -----------------------------------------------------------------------------
SELECT 
    c.state,
    c.city,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(od.line_total), 2) AS total_revenue,
    ROUND(AVG(od.line_total), 2) AS avg_order_value
FROM Orders o
JOIN Order_Details od ON o.order_id = od.order_id
JOIN Customers c ON o.customer_id = c.customer_id
GROUP BY c.state, c.city
ORDER BY total_revenue DESC;


-- -----------------------------------------------------------------------------
-- Q6: AVERAGE ORDER VALUE (AOV) BY CUSTOMER TYPE
-- Compares spending profiles of New, Recurring, and VIP customers
-- -----------------------------------------------------------------------------
SELECT 
    c.customer_type,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(od.line_total), 2) AS total_spending,
    ROUND(SUM(od.line_total) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Details od ON o.order_id = od.order_id
GROUP BY c.customer_type
ORDER BY total_spending DESC;


-- -----------------------------------------------------------------------------
-- Q7: REPEAT CUSTOMER ANALYSIS & REPEAT RATE PERCENTAGE
-- Identifies customer retention: one-time buyers vs repeat buyers
-- -----------------------------------------------------------------------------
WITH CustomerOrderCounts AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS order_count,
        SUM(total_amount) AS total_spend
    FROM Orders
    GROUP BY customer_id
)
SELECT 
    COUNT(CASE WHEN order_count = 1 THEN 1 END) AS one_time_customers,
    COUNT(CASE WHEN order_count > 1 THEN 1 END) AS repeat_customers,
    COUNT(*) AS total_customers,
    ROUND((COUNT(CASE WHEN order_count > 1 THEN 1 END) / COUNT(*)) * 100, 2) AS repeat_customer_rate_percent
FROM CustomerOrderCounts;


-- -----------------------------------------------------------------------------
-- Q8: TOP 10 CUSTOMERS BY LIFETIME SPENDING (LTV Ranking)
-- -----------------------------------------------------------------------------
SELECT 
    c.customer_id,
    c.customer_name,
    c.city,
    c.customer_type,
    COUNT(DISTINCT o.order_id) AS total_orders_placed,
    ROUND(SUM(od.line_total), 2) AS lifetime_spending
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Details od ON o.order_id = od.order_id
GROUP BY c.customer_id, c.customer_name, c.city, c.customer_type
ORDER BY lifetime_spending DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- Q9: PAYMENT METHOD POPULARITY & REVENUE CONTRIBUTION
-- -----------------------------------------------------------------------------
SELECT 
    o.payment_mode,
    COUNT(DISTINCT o.order_id) AS total_transactions,
    ROUND(SUM(od.line_total), 2) AS total_revenue,
    ROUND((SUM(od.line_total) / (SELECT SUM(line_total) FROM Order_Details)) * 100, 2) AS revenue_share_percent
FROM Orders o
JOIN Order_Details od ON o.order_id = od.order_id
GROUP BY o.payment_mode
ORDER BY total_revenue DESC;


-- -----------------------------------------------------------------------------
-- Q10: CUSTOMER SPENDING SEGMENTATION (High Value, Regular, Low Value)
-- Classifies customers dynamically based on total spend threshold
-- -----------------------------------------------------------------------------
WITH CustomerSpending AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        ROUND(SUM(od.line_total), 2) AS total_spend
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN Order_Details od ON o.order_id = od.order_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT 
    CASE 
        WHEN total_spend >= 1500 THEN 'High Value (>=$1500)'
        WHEN total_spend BETWEEN 500 AND 1499.99 THEN 'Regular ($500-$1499)'
        ELSE 'Low Value (<$500)'
    END AS customer_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(SUM(total_spend), 2) AS segment_revenue,
    ROUND(AVG(total_spend), 2) AS avg_segment_spend
FROM CustomerSpending
GROUP BY customer_segment
ORDER BY segment_revenue DESC;
