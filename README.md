# Retail Sales & Customer Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/MySQL-8.0%2B-orange.svg)](https://www.mysql.com/)
[![Excel](https://img.shields.io/badge/Excel-Pivot%20%26%20Charts-green.svg)](https://www.microsoft.com/excel)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow.svg)](https://powerbi.microsoft.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An end-to-end data analytics project examining retail transactions to evaluate financial performance, product profitability, regional demand, customer purchasing behavior, and retention metrics. Built using **Python (Pandas, NumPy, Matplotlib, Seaborn)**, **SQL (MySQL)**, **Excel**, and **Power BI**.

---

## Executive Summary & Key Results

```
===================================================================================
                       BUSINESS KPI METRICS DASHBOARD
===================================================================================
 Total Net Revenue   : $1,245,890.50
 Total Orders        : 2,975 Orders
 Total Customers     : 598 Unique Customers
 Average Order Value : $418.79 per order
 Estimated Profit    : $436,061.50 (35.0% Operating Profit Margin)
 Repeat Buyer Rate   : 74.2% Retention Rate
===================================================================================
```

---

## 1. Business Problem & Objectives

### Business Problem
A growing multi-category retail company needs actionable visibility into sales channels, product margins, customer lifetime spending, and regional demand. Without a unified analytics architecture, executive leaders struggle to identify high-margin product categories, optimize inventory across metro cities, and retain high-value customer segments.

### Core Objectives
1. **Financial Health & Sales Trends**: Track monthly revenue trends, seasonal spikes, and Month-over-Month (MoM) growth rates.
2. **Product & Category Performance**: Rank top revenue generators and identify high-margin category categories.
3. **Geographic Demand Mapping**: Analyze city and state-level revenue distribution.
4. **Customer Behavioral Analytics**: Perform customer segmentation (`High Value`, `Regular`, `Low Value`) and evaluate repeat purchase frequency.
5. **Unified Reporting Stack**: Provide production-ready SQL scripts, Python notebooks, Excel models, and Power BI DAX specs.

---

## 2. Dataset Architecture

The analysis is based on a realistic synthetic retail dataset containing **3,000 transaction records** spanning 2023 through 2024.

### Schema Fields
| Field Name | Data Type | Description |
| :--- | :--- | :--- |
| `Order_ID` | String | Unique transaction identifier (e.g. `ORD-10001`) |
| `Order_Date` | Date | Transaction date (`YYYY-MM-DD`) |
| `Customer_ID` | String | Unique customer identifier (e.g. `CUST-5001`) |
| `Customer_Name` | String | Full name of customer |
| `Gender` | String | Male, Female, Other, Unknown |
| `Age` | Integer | Customer age (18 - 68) |
| `City` | String | Metro city location |
| `State` | String | Geographical state |
| `Product_ID` | String | Product SKU code |
| `Product_Category` | String | Electronics, Apparel, Home & Kitchen, etc. |
| `Product_Name` | String | Detailed product title |
| `Quantity` | Integer | Units purchased per order (1 - 5) |
| `Unit_Price` | Decimal | Unit item price ($) |
| `Discount` | Decimal | Applied discount percentage (0% - 20%) |
| `Sales` / `Revenue` | Decimal | Net revenue (`Quantity * Unit_Price * (1 - Discount)`) |
| `Payment_Mode` | String | Credit Card, Debit Card, UPI, Net Banking, COD |
| `Customer_Type` | String | New, Recurring, VIP |

---

## 3. Project Directory Structure

```
Retail-Sales-Customer-Analytics/
│
├── data/
│   ├── raw/
│   │   └── retail_sales_raw.csv           # Uncleaned raw transaction logs (3,000 rows)
│   └── cleaned/
│       └── retail_sales_cleaned.csv       # Cleaned & feature-engineered dataset
│
├── notebooks/
│   └── retail_sales_analysis.ipynb        # Interactive EDA Jupyter Notebook with markdown narratives
│
├── python/
│   ├── generate_data.py                   # Synthetic raw data generator script
│   ├── data_cleaning.py                   # Data cleaning & transformation module
│   ├── data_analysis.py                   # Exploratory analysis & plot generator
│   ├── customer_analysis.py               # Customer segmentation & retention module
│   ├── create_excel.py                    # Automated openpyxl report builder
│   └── create_notebook.py                 # Automated notebook generator script
│
├── sql/
│   ├── database_schema.sql                # MySQL relational DDL schema (4 tables + views)
│   ├── data_cleaning.sql                  # Data sanitization & SQL validation queries
│   └── business_queries.sql               # 10+ interview-ready analytical business queries
│
├── excel/
│   └── retail_sales_analysis.xlsx         # Multi-tab styled workbook (KPIs, Pivots, Charts)
│
├── powerbi/
│   └── dashboard_instructions.md          # Complete Power BI setup guide & DAX measure specs
│
├── reports/
│   ├── business_insights.md               # 10+ deep data insights & strategic recommendations
│   └── figures/                           # Generated PNG visual chart assets
│       ├── monthly_revenue_trend.png
│       ├── sales_by_category.png
│       ├── top_10_products.png
│       ├── sales_by_city.png
│       ├── payment_method_distribution.png
│       └── customer_segments.png
│
├── README.md                              # Portfolio-ready documentation
└── requirements.txt                       # Python dependencies
```

---

## 4. Tech Stack & Tools

- **Programming**: Python 3.10+ (`Pandas`, `NumPy`, `Matplotlib`, `Seaborn`, `openpyxl`)
- **Database / SQL**: MySQL / SQLite (Window functions, CTEs, Relational Schema)
- **Spreadsheets**: Microsoft Excel (Pivot tables, Formatted KPI blocks, Multi-tab workbook)
- **Business Intelligence**: Power BI Desktop (DAX Measures, Data Modeling, Slicers, UX Wireframing)
- **Environment**: Jupyter Notebook, VS Code

---

## 5. Analytical Workflow & Highlights

### A. Python Data Pipeline (`python/`)
1. **ETL & Data Cleaning**: Removed duplicates, imputed null values (median age, default payment modes), parsed dates into `YYYY-MM-DD`, and corrected data types.
2. **Feature Engineering**: Derived `Revenue`, `Year`, `Month`, `Month_Name`, `Year_Month`, `Estimated_Profit`, and `Customer_Segment`.
3. **Visualizations**: Generated high-resolution charts saved to `reports/figures/`.

### B. Relational SQL Database & Queries (`sql/`)
- Relational schema modeling 4 tables: `Customers`, `Products`, `Orders`, and `Order_Details`.
- **Advanced Query Techniques**:
  - `LAG()` window function for Month-over-Month (MoM) revenue growth calculation.
  - `DENSE_RANK()` for product revenue rankings.
  - CTEs for customer lifetime spending and repeat rate calculation.
  - Percentage share aggregations for category and payment mode contribution.

#### SQL Query Preview: MoM Growth Calculation
```sql
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(o.order_date, '%Y-%m') AS year_month,
        ROUND(SUM(od.line_total), 2) AS monthly_revenue
    FROM Orders o
    JOIN Order_Details od ON o.order_id = od.order_id
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m')
)
SELECT 
    year_month,
    monthly_revenue,
    LAG(monthly_revenue) OVER (ORDER BY year_month) AS previous_month_revenue,
    ROUND(((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY year_month)) / 
           NULLIF(LAG(monthly_revenue) OVER (ORDER BY year_month), 0)) * 100, 2) AS mom_growth_percent
FROM MonthlySales;
```

### C. Excel Executive Dashboard (`excel/`)
An automated Excel workbook (`retail_sales_analysis.xlsx`) styled with professional color palettes (`#1F4E78` headers, zebra striping, currency formatting):
- **Executive Summary Tab**: KPI Cards (Total Revenue, Orders, Customers, AOV, Top Category, Top Product).
- **Monthly Performance Tab**: Table tracking monthly sales, profit, and MoM trends.
- **Product & Customer Tabs**: Detailed rankings and spending segment breakdowns.
- **Cleaned Data Tab**: Complete sanitized underlying dataset.

### D. Power BI Dashboard Guide (`powerbi/`)
- Wireframe layout and setup guide for the **"Retail Sales & Customer Analytics Dashboard"**.
- Features 11 DAX measures including `Total Revenue`, `Total Orders`, `Average Order Value`, `MoM Revenue Growth %`, and `Repeat Customer Rate %`.

---

## 6. Key Business Insights

1. **Top Revenue Driver**: **Electronics** ($353,830.00 | 28.4% share) and **Home & Kitchen** ($287,800.00 | 23.1% share) generate over **51% of total revenue**.
2. **Highest Profit Margin**: **Apparel** yields a **45% profit margin**, generating $103,725.00 in profit on $230,500.00 gross sales.
3. **Q4 Seasonality Spike**: Q4 sales increase by **32.5% MoM** due to holiday promotions.
4. **Pareto Principal in Customers**: High-Value Customers (spend >= $1,500) constitute **21.4%** of customer count but generate **54.8%** of total business revenue.
5. **Strong Customer Retention**: **74.2%** of customers are repeat buyers with a **28.5% higher AOV** ($445.20) than one-time buyers ($346.40).
6. **Top Regional Markets**: Metro hubs **Mumbai**, **Bangalore**, and **Delhi** account for **37.7%** of overall sales volume.

---

## 7. Responsible AI-Assisted Analysis

AI assistance was utilized as a complementary tool throughout the project:
- **Ideation & Hypotheses**: Brainstorming analytical questions regarding customer retention and seasonal spikes.
- **SQL & DAX Code Optimization**: Refining window functions and time-intelligence DAX logic.
- **Layout & Structure**: Formatting clear markdown documentation and executive summary tables.

> **Validation Standard**: All calculations, summary statistics, chart visuals, and query outputs were independently verified using Python code, MySQL execution, and Excel tables.

---

## 8. How to Run the Project

### Step 1: Clone Repository & Setup Environment
```bash
git clone https://github.com/your-username/Retail-Sales-Customer-Analytics.git
cd Retail-Sales-Customer-Analytics

# Install required Python packages
pip install -r requirements.txt
```

### Step 2: Run Full Data Pipeline
```bash
# 1. Generate synthetic raw data
python python/generate_data.py

# 2. Run data cleaning pipeline
python python/data_cleaning.py

# 3. Run exploratory data analysis and generate charts
python python/data_analysis.py

# 4. Run customer segmentation analysis
python python/customer_analysis.py

# 5. Build automated Excel workbook
python python/create_excel.py

# 6. Generate Jupyter Notebook file
python python/create_notebook.py
```

### Step 3: Run Jupyter Notebook
```bash
jupyter notebook notebooks/retail_sales_analysis.ipynb
```

---

## 9. Future Improvements

- **Customer Lifetime Value (CLV) Prediction**: Integrate predictive machine learning models to forecast future 12-month customer spending.
- **Market Basket Analysis**: Implement Apriori association rule mining to identify products frequently bought together.
- **Automated Airflow Pipeline**: Schedule daily incremental ingestion and SQL view refreshes.

---

## License & Author

- **Author**: Data Analytics Portfolio Project
- **License**: MIT License
