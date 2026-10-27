"""
Retail Sales & Customer Analytics - Customer Analytics Module
================================================================
Performs customer-level behavior analysis, spending distribution,
frequency segmentation, repeat customer identification, and visual charts.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_cleaned_data(filepath="data/cleaned/retail_sales_cleaned.csv"):
    df = pd.read_csv(filepath)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

def analyze_customer_metrics(df):
    """Aggregate customer-level metrics."""
    customer_df = df.groupby('Customer_ID').agg(
        Customer_Name=('Customer_Name', 'first'),
        Gender=('Gender', 'first'),
        Age=('Age', 'first'),
        City=('City', 'first'),
        State=('State', 'first'),
        Customer_Type=('Customer_Type', 'first'),
        Total_Spend=('Revenue', 'sum'),
        Total_Orders=('Order_ID', 'nunique'),
        Total_Items=('Quantity', 'sum'),
        Avg_Order_Value=('Revenue', 'mean'),
        First_Purchase=('Order_Date', 'min'),
        Last_Purchase=('Order_Date', 'max')
    ).reset_index()

    # Recalculate segment explicitly
    customer_df['Segment'] = np.where(
        customer_df['Total_Spend'] >= 1500, 'High Value',
        np.where(customer_df['Total_Spend'] >= 500, 'Regular', 'Low Value')
    )

    customer_df['Is_Repeat'] = customer_df['Total_Orders'] > 1

    print("==================================================")
    print("            CUSTOMER ANALYTICS SUMMARY            ")
    print("==================================================")
    print(f"Total Unique Customers: {len(customer_df)}")
    repeat_count = customer_df['Is_Repeat'].sum()
    repeat_rate = (repeat_count / len(customer_df)) * 100
    print(f"One-time Customers: {len(customer_df) - repeat_count} ({(100 - repeat_rate):.1f}%)")
    print(f"Repeat Customers: {repeat_count} ({repeat_rate:.1f}%)")
    print("\nSegment Breakdown:")
    segment_summary = customer_df.groupby('Segment').agg(
        Count=('Customer_ID', 'count'),
        Total_Revenue=('Total_Spend', 'sum'),
        Avg_Spend=('Total_Spend', 'mean')
    ).reset_index()
    for _, row in segment_summary.iterrows():
        print(f" - {row['Segment']}: {row['Count']} customers | Total Spend: ${row['Total_Revenue']:,.2f} | Avg Spend: ${row['Avg_Spend']:,.2f}")
    print("==================================================\n")

    return customer_df

def plot_customer_segments(customer_df, output_dir="reports/figures"):
    """Plot customer segment distribution and revenue contribution."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Segment Customer Count
    seg_counts = customer_df['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    sns.barplot(data=seg_counts, x='Segment', y='Count', palette="Set2", ax=ax1)
    ax1.set_title("Customer Count by Segment", fontweight='bold')
    ax1.set_xlabel("Segment")
    ax1.set_ylabel("Number of Customers")

    # Segment Total Revenue
    seg_rev = customer_df.groupby('Segment')['Total_Spend'].sum().reset_index()
    sns.barplot(data=seg_rev, x='Segment', y='Total_Spend', palette="Set2", ax=ax2)
    ax2.set_title("Revenue Contribution by Segment ($)", fontweight='bold')
    ax2.set_xlabel("Segment")
    ax2.set_ylabel("Total Revenue ($)")

    for ax in [ax1, ax2]:
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f"{height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9)

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    fig_path = os.path.join(output_dir, "customer_segments.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[*] Saved plot: {fig_path}")

def run_customer_pipeline(cleaned_path="data/cleaned/retail_sales_cleaned.csv"):
    df = load_cleaned_data(cleaned_path)
    customer_df = analyze_customer_metrics(df)
    plot_customer_segments(customer_df)
    return customer_df

if __name__ == "__main__":
    run_customer_pipeline()
