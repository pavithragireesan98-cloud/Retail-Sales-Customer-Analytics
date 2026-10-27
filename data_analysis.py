"""
Retail Sales & Customer Analytics - Data Analysis & Visualization Module
========================================================================
Performs exploratory data analysis (EDA), generates summary metrics,
and creates publication-ready visualizations saved to disk.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual aesthetic style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

def load_cleaned_data(filepath="data/cleaned/retail_sales_cleaned.csv"):
    """Load cleaned dataset."""
    df = pd.read_csv(filepath)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

def generate_summary_metrics(df):
    """Compute top-level business KPI metrics."""
    total_revenue = df['Revenue'].sum()
    total_orders = df['Order_ID'].nunique()
    total_customers = df['Customer_ID'].nunique()
    aov = total_revenue / total_orders
    total_profit = df['Estimated_Profit'].sum()

    metrics = {
        "Total Revenue ($)": round(total_revenue, 2),
        "Total Orders": total_orders,
        "Total Customers": total_customers,
        "Average Order Value ($)": round(aov, 2),
        "Estimated Profit ($)": round(total_profit, 2)
    }

    print("==================================================")
    print("           EXECUTIVE SUMMARY METRICS              ")
    print("==================================================")
    for k, v in metrics.items():
        print(f" - {k}: {v:,.2f}" if isinstance(v, float) else f" - {k}: {v:,}")
    print("==================================================\n")
    return metrics

def plot_monthly_revenue(df, output_dir="reports/figures"):
    """Generate Monthly Revenue Trend plot."""
    monthly_sales = df.groupby('Year_Month')['Revenue'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly_sales['Year_Month'], monthly_sales['Revenue'] / 1000, 
            marker='o', color='#1f77b4', linewidth=2.5, markersize=7)
    
    ax.set_title("Monthly Revenue Trend (in $ Thousands)", pad=15, fontweight='bold')
    ax.set_xlabel("Year-Month", labelpad=10)
    ax.set_ylabel("Revenue ($K)", labelpad=10)
    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    fig_path = os.path.join(output_dir, "monthly_revenue_trend.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[*] Saved plot: {fig_path}")

def plot_category_sales(df, output_dir="reports/figures"):
    """Generate Sales by Category plot."""
    cat_sales = df.groupby('Product_Category')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    palette = sns.color_palette("Blues_r", len(cat_sales))
    bars = sns.barplot(data=cat_sales, x='Revenue', y='Product_Category', palette=palette, ax=ax)

    # Annotate bar values
    for p in bars.patches:
        width = p.get_width()
        ax.annotate(f"${width:,.0f}", (width, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=10)

    ax.set_title("Revenue by Product Category", pad=15, fontweight='bold')
    ax.set_xlabel("Revenue ($)", labelpad=10)
    ax.set_ylabel("Category", labelpad=10)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, "sales_by_category.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[*] Saved plot: {fig_path}")

def plot_top_products(df, output_dir="reports/figures"):
    """Generate Top 10 Products by Revenue plot."""
    top_prod = df.groupby(['Product_Name', 'Product_Category'])['Revenue'].sum().reset_index()
    top_prod = top_prod.sort_values('Revenue', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = sns.barplot(data=top_prod, x='Revenue', y='Product_Name', palette="viridis", ax=ax)

    for p in bars.patches:
        width = p.get_width()
        ax.annotate(f"${width:,.0f}", (width, p.get_y() + p.get_height() / 2.),
                    ha='left', va='center', xytext=(5, 0), textcoords='offset points', fontsize=9)

    ax.set_title("Top 10 Products by Total Revenue", pad=15, fontweight='bold')
    ax.set_xlabel("Revenue ($)", labelpad=10)
    ax.set_ylabel("Product Name", labelpad=10)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, "top_10_products.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[*] Saved plot: {fig_path}")

def plot_city_performance(df, output_dir="reports/figures"):
    """Generate Revenue by City plot."""
    city_sales = df.groupby('City')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = sns.barplot(data=city_sales, x='City', y='Revenue', palette="rocket", ax=ax)

    for p in bars.patches:
        height = p.get_height()
        ax.annotate(f"${height:,.0f}", (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9)

    ax.set_title("Revenue Distribution across Metro Cities", pad=15, fontweight='bold')
    ax.set_xlabel("City", labelpad=10)
    ax.set_ylabel("Revenue ($)", labelpad=10)
    plt.xticks(rotation=30)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, "sales_by_city.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[*] Saved plot: {fig_path}")

def plot_payment_methods(df, output_dir="reports/figures"):
    """Generate Payment Method breakdown plot."""
    pay_dist = df.groupby('Payment_Mode')['Revenue'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(7, 7))
    colors = ['#4c72b0', '#55a868', '#c44e52', '#8172b0', '#ccb974']
    wedges, texts, autotexts = ax.pie(
        pay_dist['Revenue'], 
        labels=pay_dist['Payment_Mode'], 
        autopct='%1.1f%%', 
        startangle=140,
        colors=colors,
        textprops=dict(color="black")
    )
    plt.setp(autotexts, size=10, weight="bold")
    ax.set_title("Revenue Share by Payment Method", pad=15, fontweight='bold')
    plt.tight_layout()

    fig_path = os.path.join(output_dir, "payment_method_distribution.png")
    plt.savefig(fig_path, dpi=300)
    plt.close()
    print(f"[*] Saved plot: {fig_path}")

def run_analysis_pipeline(cleaned_path="data/cleaned/retail_sales_cleaned.csv"):
    df = load_cleaned_data(cleaned_path)
    generate_summary_metrics(df)
    plot_monthly_revenue(df)
    plot_category_sales(df)
    plot_top_products(df)
    plot_city_performance(df)
    plot_payment_methods(df)

if __name__ == "__main__":
    run_analysis_pipeline()
