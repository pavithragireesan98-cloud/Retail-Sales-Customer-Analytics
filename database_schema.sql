-- =============================================================================
-- RETAIL SALES & CUSTOMER ANALYTICS DATABASE SCHEMA (MySQL Compatible)
-- Project: End-to-End Retail Analytics
-- Author: Data Analytics Portfolio
-- =============================================================================

CREATE DATABASE IF NOT EXISTS retail_analytics_db;
USE retail_analytics_db;

-- -----------------------------------------------------------------------------
-- 1. Table: Customers
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS Order_Details;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    age INT CHECK (age >= 18 AND age <= 100),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    customer_type VARCHAR(20) DEFAULT 'Regular',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_customers_city ON Customers(city);
CREATE INDEX idx_customers_type ON Customers(customer_type);

-- -----------------------------------------------------------------------------
-- 2. Table: Products
-- -----------------------------------------------------------------------------
CREATE TABLE Products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    is_active BOOLEAN DEFAULT TRUE
);

-- Indexes
CREATE INDEX idx_products_category ON Products(product_category);

-- -----------------------------------------------------------------------------
-- 3. Table: Orders
-- -----------------------------------------------------------------------------
CREATE TABLE Orders (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    payment_mode VARCHAR(30),
    total_amount DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_orders_date ON Orders(order_date);
CREATE INDEX idx_orders_customer ON Orders(customer_id);

-- -----------------------------------------------------------------------------
-- 4. Table: Order_Details
-- -----------------------------------------------------------------------------
CREATE TABLE Order_Details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10, 2) NOT NULL,
    discount DECIMAL(4, 2) DEFAULT 0.00 CHECK (discount >= 0.00 AND discount <= 1.00),
    line_total DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * unit_price * (1 - discount)) STORED,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE RESTRICT
);

-- Indexes
CREATE INDEX idx_order_details_order ON Order_Details(order_id);
CREATE INDEX idx_order_details_product ON Order_Details(product_id);

-- -----------------------------------------------------------------------------
-- Unified Flat Analytics View
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_retail_sales_master AS
SELECT 
    o.order_id,
    o.order_date,
    YEAR(o.order_date) AS order_year,
    MONTH(o.order_date) AS order_month,
    MONTHNAME(o.order_date) AS month_name,
    c.customer_id,
    c.customer_name,
    c.gender,
    c.age,
    c.city,
    c.state,
    c.customer_type,
    p.product_id,
    p.product_category,
    p.product_name,
    od.quantity,
    od.unit_price,
    od.discount,
    od.line_total AS sales_revenue,
    o.payment_mode
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Order_Details od ON o.order_id = od.order_id
JOIN Products p ON od.product_id = p.product_id;
