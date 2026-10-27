# Power BI Dashboard Specification & Setup Guide

## Project Title: Retail Sales & Customer Analytics Dashboard

This document provides complete, step-by-step technical instructions for recreating the **Retail Sales & Customer Analytics Dashboard** in Power BI Desktop.

---

## 1. Data Connection & Modeling

### Data Import
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select `data/cleaned/retail_sales_cleaned.csv`.
4. In Power Query Editor:
   - Ensure `Order_Date` is set to **Date** format.
   - Ensure `Revenue`, `Unit_Price`, `Discount`, `Estimated_Profit` are set to **Fixed Decimal Number** (`$`).
   - Ensure `Quantity`, `Age` are set to **Whole Number**.
   - Click **Close & Apply**.

### Calendar Table Creation (DAX)
To enable accurate Time Intelligence calculations, create a dedicated `Calendar` table:
```dax
Calendar = 
ADDCOLUMNS (
    CALENDAR(DATE(2023, 1, 1), DATE(2024, 12, 31)),
    "Year", YEAR([Date]),
    "MonthNo", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMM"),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & FORMAT([Date], "Q")
)
```
- **Relationship**: Create a 1-to-Many relationship between `Calendar[Date]` and `retail_sales_cleaned[Order_Date]`.

---

## 2. DAX Measures Specification

Create a new table named `_Measures` and add the following DAX calculations:

### 1. Total Revenue
```dax
Total Revenue = SUM(retail_sales_cleaned[Revenue])
```

### 2. Total Orders
```dax
Total Orders = DISTINCTCOUNT(retail_sales_cleaned[Order_ID])
```

### 3. Total Customers
```dax
Total Customers = DISTINCTCOUNT(retail_sales_cleaned[Customer_ID])
```

### 4. Average Order Value (AOV)
```dax
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

### 5. Estimated Total Profit
```dax
Total Profit = SUM(retail_sales_cleaned[Estimated_Profit])
```

### 6. Profit Margin %
```dax
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)
```

### 7. Prior Month Revenue (PM Revenue)
```dax
PM Revenue = 
CALCULATE(
    [Total Revenue],
    DATEADD('Calendar'[Date], -1, MONTH)
)
```

### 8. Month-over-Month (MoM) Revenue Growth %
```dax
MoM Revenue Growth % = 
VAR PrevRev = [PM Revenue]
RETURN
DIVIDE([Total Revenue] - PrevRev, PrevRev, 0)
```

### 9. Repeat Customer Count
```dax
Repeat Customers = 
COUNTROWS(
    FILTER(
        VALUES(retail_sales_cleaned[Customer_ID]),
        CALCULATE(DISTINCTCOUNT(retail_sales_cleaned[Order_ID])) > 1
    )
)
```

### 10. Repeat Customer Rate %
```dax
Repeat Customer Rate % = DIVIDE([Repeat Customers], [Total Customers], 0)
```

### 11. Customer Revenue Contribution %
```dax
Customer Contribution % = 
DIVIDE(
    [Total Revenue],
    CALCULATE([Total Revenue], ALL(retail_sales_cleaned[Customer_ID])),
    0
)
```

---

## 3. Canvas Layout & Visual Configuration

### Theme & Color Palette
- **Background**: `#F8F9FA` (Soft Light Gray)
- **Primary Header / Cards**: `#1F4E78` (Navy Blue)
- **Accent Color**: `#2E75B6` / `#00B0F0` (Vibrant Blue)
- **Secondary Accent**: `#ED7D31` (Warm Orange)
- **Font Family**: Segoe UI / Din Neutral

---

### Dashboard Wireframe Structure

```
+-----------------------------------------------------------------------------------------------+
| HEADER BAR: Retail Sales & Customer Analytics Dashboard              [ Logo / Date Updated ]  |
+-----------------------------------------------------------------------------------------------+
| SLICERS BAR: [ Date Range ] | [ Category ] | [ City/State ] | [ Gender ] | [ Customer Type ] |
+-------------------------------+-------------------------------+-------------------------------+
| KPI CARD 1: Total Revenue    | KPI CARD 2: Total Orders      | KPI CARD 3: Total Customers   |
| $1,245,890.00 (+12.4% MoM)   | 2,975 Orders                  | 598 Unique Customers          |
+-------------------------------+-------------------------------+-------------------------------+
| KPI CARD 4: Avg Order Value  | KPI CARD 5: Total Profit      | KPI CARD 6: Repeat Rate       |
| $418.78                       | $436,061.50 (35.0% Margin)    | 74.2% Repeat Customers        |
+-------------------------------+-------------------------------+-------------------------------+
| VISUAL 1: Line Chart          | VISUAL 2: Donut Chart         | VISUAL 3: Clustered Bar Chart  |
| Monthly Revenue & MoM Trend   | Revenue Share by Category     | Top 10 Revenue Products       |
+-------------------------------+-------------------------------+-------------------------------+
| VISUAL 4: Map / Bar Chart     | VISUAL 5: Column Chart        | VISUAL 6: Donut Chart         |
| Revenue by City & State       | Revenue by Customer Segment   | Payment Method Breakdown      |
+-----------------------------------------------------------------------------------------------+
```

---

## 4. Visual Elements Configuration Steps

### 1. Header Banner
- Add a **Shape (Rectangle)** across the top canvas width.
- Fill: `#1F4E78`. Title Text: `"Retail Sales & Customer Analytics Dashboard"` in white Segoe UI Bold (20pt).

### 2. KPI Card Visuals (Top Row)
- **Card 1 (Total Revenue)**: Metric `[Total Revenue]`. Subtitle: `[MoM Revenue Growth %]`. Format: Currency (`$#,##0`).
- **Card 2 (Total Orders)**: Metric `[Total Orders]`. Format: Whole number.
- **Card 3 (Total Customers)**: Metric `[Total Customers]`. Format: Whole number.
- **Card 4 (Average Order Value)**: Metric `[Average Order Value]`. Format: Currency (`$#,##0.00`).

### 3. Visual 1: Monthly Revenue Trend
- **Type**: Area / Line Chart
- **X-Axis**: `Calendar[YearMonth]`
- **Y-Axis**: `[Total Revenue]`
- **Data Labels**: Enabled (In Thousands `$K`)

### 4. Visual 2: Category Revenue Breakdown
- **Type**: Donut Chart / Treemap
- **Legend**: `retail_sales_cleaned[Product_Category]`
- **Values**: `[Total Revenue]`
- **Detail Labels**: Category + Percent of Total

### 5. Visual 3: Top 10 Products
- **Type**: Clustered Bar Chart
- **Y-Axis**: `retail_sales_cleaned[Product_Name]` (Filtered to Top 10 by `Total Revenue` in Filters pane)
- **X-Axis**: `[Total Revenue]`
- **Data Color**: `#1F4E78`

### 6. Visual 4: City Sales Performance
- **Type**: Clustered Column Chart / Filled Map
- **X-Axis / Location**: `retail_sales_cleaned[City]`
- **Y-Axis**: `[Total Revenue]`

### 7. Visual 5: Customer Segment Analysis
- **Type**: Stacked Column Chart
- **X-Axis**: `retail_sales_cleaned[Customer_Segment]` (`High Value`, `Regular`, `Low Value`)
- **Y-Axis**: `[Total Revenue]` & `[Total Customers]`

### 8. Visual 6: Payment Method Breakdown
- **Type**: Donut Chart
- **Legend**: `retail_sales_cleaned[Payment_Mode]`
- **Values**: `[Total Revenue]`

---

## 5. Interactive Slicers

Place these slicers horizontally along the top control panel:
1. **Date Range Slicer**: `Calendar[Date]` (Between mode).
2. **Product Category Slicer**: `retail_sales_cleaned[Product_Category]` (Dropdown).
3. **Location Slicer**: `retail_sales_cleaned[State]` / `[City]` (Dropdown).
4. **Gender Slicer**: `retail_sales_cleaned[Gender]` (Tile mode).
5. **Customer Type Slicer**: `retail_sales_cleaned[Customer_Type]` (Dropdown).
6. **Payment Mode Slicer**: `retail_sales_cleaned[Payment_Mode]` (Dropdown).

---

## 6. Portfolio Presentation Tips

- Enable **Edit Interactions** to ensure slicers cross-filter all visuals seamlessly.
- Add visual tooltips showing **Profit Margin %** when hovering over product category bars.
- Export as high-resolution screenshots for GitHub README inclusion.
