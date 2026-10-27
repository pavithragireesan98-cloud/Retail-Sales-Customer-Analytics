"""
Retail Sales & Customer Analytics - Data Cleaning Module
=========================================================
This module handles loading raw retail sales data, inspecting schema & nulls,
removing duplicates, correcting data types, parsing dates, imputing missing values,
calculating derived columns, and exporting the cleaned dataset.
"""

import os
import pandas as pd
import numpy as np

def load_raw_data(filepath="data/raw/retail_sales_raw.csv"):
    """Load raw dataset from CSV file."""
    print(f"[*] Loading raw dataset from: {filepath}")
    df = pd.read_csv(filepath)
    print(f"    Raw data shape: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def inspect_data(df):
    """Print initial data summary, missing value report, and duplicate count."""
    print("\n--- Data Exploration & Missing Value Summary ---")
    print(f"Total Rows: {len(df)}")
    print(f"Duplicate Rows Count: {df.duplicated().sum()}")
    print("\nMissing Values per Column:")
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0])
    return null_counts

def clean_data(df):
    """
    Perform full data cleaning and feature engineering.
    """
    print("\n[*] Starting Data Cleaning Pipeline...")
    df_clean = df.copy()

    # 1. Remove duplicate records
    init_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    print(f"    [1] Removed {init_rows - len(df_clean)} duplicate rows. Current rows: {len(df_clean)}")

    # 2. Handle & parse Order_Date to datetime YYYY-MM-DD
    df_clean['Order_Date'] = pd.to_datetime(df_clean['Order_Date'], errors='coerce', format='mixed')
    # Impute any invalid/unparseable dates with median date
    if df_clean['Order_Date'].isnull().sum() > 0:
        median_date = df_clean['Order_Date'].dropna().median()
        df_clean['Order_Date'] = df_clean['Order_Date'].fillna(median_date)
    print("    [2] Standardized Order_Date to datetime format.")

    # 3. Standardize text fields (Gender, Payment_Mode, City, State)
    df_clean['Gender'] = df_clean['Gender'].astype(str).str.strip().str.title()
    df_clean['Gender'] = df_clean['Gender'].replace({'Nan': np.nan, 'None': np.nan, '': np.nan})
    df_clean['Gender'] = df_clean['Gender'].fillna('Unknown')

    df_clean['Payment_Mode'] = df_clean['Payment_Mode'].astype(str).str.strip().str.title()
    df_clean['Payment_Mode'] = df_clean['Payment_Mode'].replace({'Nan': np.nan, 'None': np.nan, '': np.nan})
    df_clean['Payment_Mode'] = df_clean['Payment_Mode'].fillna('Credit Card')

    # 4. Handle Age missing values (Impute with median age)
    if df_clean['Age'].isnull().sum() > 0:
        median_age = df_clean['Age'].dropna().median()
        df_clean['Age'] = df_clean['Age'].fillna(median_age).astype(int)
    else:
        df_clean['Age'] = df_clean['Age'].astype(int)

    # 5. Data Type Corrections & Numeric Bounds
    df_clean['Quantity'] = df_clean['Quantity'].astype(int)
    df_clean['Unit_Price'] = df_clean['Unit_Price'].astype(float)
    df_clean['Discount'] = df_clean['Discount'].astype(float).fillna(0.0)

    # 6. Feature Creation / Recalculate Exact Revenue & Profit
    # Revenue = Quantity * Unit_Price * (1 - Discount)
    df_clean['Revenue'] = np.round(df_clean['Quantity'] * df_clean['Unit_Price'] * (1.0 - df_clean['Discount']), 2)
    
    # Feature Creation: Year, Month, Month_Name, Year_Month
    df_clean['Year'] = df_clean['Order_Date'].dt.year
    df_clean['Month'] = df_clean['Order_Date'].dt.month
    df_clean['Month_Name'] = df_clean['Order_Date'].dt.strftime('%b')
    df_clean['Year_Month'] = df_clean['Order_Date'].dt.strftime('%Y-%m')

    # Feature Creation: Estimated Profit (assuming category average margin between 25% and 40%)
    category_margins = {
        'Electronics': 0.25,
        'Apparel': 0.45,
        'Home & Kitchen': 0.35,
        'Beauty & Personal Care': 0.50,
        'Books & Stationery': 0.30,
        'Sports & Outdoors': 0.40
    }
    df_clean['Profit_Margin'] = df_clean['Product_Category'].map(category_margins).fillna(0.30)
    df_clean['Estimated_Profit'] = np.round(df_clean['Revenue'] * df_clean['Profit_Margin'], 2)

    # 7. Customer Spending Segmentation
    cust_total_spend = df_clean.groupby('Customer_ID')['Revenue'].transform('sum')
    df_clean['Customer_Segment'] = np.where(
        cust_total_spend >= 1500, 'High Value',
        np.where(cust_total_spend >= 500, 'Regular', 'Low Value')
    )

    print(f"    [3] Derived new columns: Revenue, Year, Month, Month_Name, Year_Month, Profit_Margin, Estimated_Profit, Customer_Segment.")
    print(f"[*] Data Cleaning Complete. Final Cleaned Rows: {len(df_clean)}")

    return df_clean

def save_cleaned_data(df, output_path="data/cleaned/retail_sales_cleaned.csv"):
    """Export cleaned dataframe to CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[*] Saved cleaned dataset to: {output_path}")

def run_cleaning_pipeline(raw_path="data/raw/retail_sales_raw.csv", cleaned_path="data/cleaned/retail_sales_cleaned.csv"):
    df_raw = load_raw_data(raw_path)
    inspect_data(df_raw)
    df_cleaned = clean_data(df_raw)
    save_cleaned_data(df_cleaned, cleaned_path)
    return df_cleaned

if __name__ == "__main__":
    run_cleaning_pipeline()
