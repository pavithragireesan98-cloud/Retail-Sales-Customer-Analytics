-- =============================================================================
-- RETAIL SALES & CUSTOMER ANALYTICS: DATA CLEANING & VALIDATION (SQL / MySQL)
-- =============================================================================

USE retail_analytics_db;

-- -----------------------------------------------------------------------------
-- 1. IDENTIFY MISSING VALUES
-- -----------------------------------------------------------------------------
-- Check for missing values in Customers table
SELECT 
    COUNT(*) AS total_records,
    SUM(CASE WHEN gender IS NULL OR TRIM(gender) = '' THEN 1 ELSE 0 END) AS missing_gender,
    SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS missing_age,
    SUM(CASE WHEN city IS NULL OR TRIM(city) = '' THEN 1 ELSE 0 END) AS missing_city
FROM Customers;

-- Check for missing payment modes in Orders
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN payment_mode IS NULL OR TRIM(payment_mode) = '' THEN 1 ELSE 0 END) AS missing_payment_mode
FROM Orders;

-- -----------------------------------------------------------------------------
-- 2. STANDARDIZE GENDER STRINGS & IMPUTE MISSING VALUES
-- -----------------------------------------------------------------------------
-- Standardize lowercase strings ('male' -> 'Male', 'female' -> 'Female')
UPDATE Customers
SET gender = CONCAT(UPPER(LEFT(gender, 1)), LOWER(SUBSTRING(gender, 2)))
WHERE gender IS NOT NULL;

-- Fill NULL gender with 'Unknown' or mode
UPDATE Customers
SET gender = 'Unknown'
WHERE gender IS NULL OR TRIM(gender) = '';

-- Impute NULL age with median/average age (e.g., 40)
UPDATE Customers
SET age = (SELECT ROUND(AVG(age)) FROM (SELECT age FROM Customers WHERE age IS NOT NULL) AS temp_age)
WHERE age IS NULL;

-- Impute NULL payment mode with 'Credit Card' (default mode)
UPDATE Orders
SET payment_mode = 'Credit Card'
WHERE payment_mode IS NULL OR TRIM(payment_mode) = '';

-- -----------------------------------------------------------------------------
-- 3. DETECT & REMOVE DUPLICATE ORDERS
-- -----------------------------------------------------------------------------
-- Find duplicate Order IDs if any exist
SELECT order_id, COUNT(*) AS dup_count
FROM Orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- CTE to delete duplicates keeping the lowest primary key/first record
WITH CTE_Duplicates AS (
    SELECT order_id,
           ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date ASC) AS row_num
    FROM Orders
)
DELETE FROM Orders
WHERE order_id IN (
    SELECT order_id FROM CTE_Duplicates WHERE row_num > 1
);

-- -----------------------------------------------------------------------------
-- 4. VALIDATE REVENUE & QUANTITY INTEGRITY
-- -----------------------------------------------------------------------------
-- Identify records with invalid quantity or unit price
SELECT *
FROM Order_Details
WHERE quantity <= 0 OR unit_price <= 0 OR discount < 0 OR discount > 1.0;

-- Recalculate and update order totals in Orders table
UPDATE Orders o
SET total_amount = (
    SELECT COALESCE(SUM(od.line_total), 0)
    FROM Order_Details od
    WHERE od.order_id = o.order_id
);

-- -----------------------------------------------------------------------------
-- 5. FINAL DATA INTEGRITY SANITY CHECK
-- -----------------------------------------------------------------------------
SELECT 
    (SELECT COUNT(*) FROM Customers) AS clean_customer_count,
    (SELECT COUNT(*) FROM Products) AS clean_product_count,
    (SELECT COUNT(*) FROM Orders) AS clean_order_count,
    (SELECT COUNT(*) FROM Order_Details) AS clean_order_detail_count;
