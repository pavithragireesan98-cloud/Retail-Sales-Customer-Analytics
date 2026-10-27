"""
Retail Sales & Customer Analytics - Automated Excel Report Generator
====================================================================
Generates a multi-tab, professionally styled Excel workbook (retail_sales_analysis.xlsx)
featuring an Executive KPI Summary, Monthly Performance, Category & Product Breakdown,
and Customer Segmentation.
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_report(cleaned_path="data/cleaned/retail_sales_cleaned.csv", output_path="excel/retail_sales_analysis.xlsx"):
    print(f"[*] Reading cleaned dataset from {cleaned_path} for Excel report generation...")
    df = pd.read_csv(cleaned_path)
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styling Palette
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid") # Dark Navy
    kpi_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")    # Soft Soft Blue
    zebra_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")  # Very Light Gray Blue
    
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    title_font = Font(name="Calibri", size=16, bold=True, color="1F4E78")
    section_font = Font(name="Calibri", size=13, bold=True, color="1F4E78")
    bold_font = Font(name="Calibri", size=11, bold=True)
    regular_font = Font(name="Calibri", size=11)
    kpi_val_font = Font(name="Calibri", size=14, bold=True, color="1F4E78")

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    # -------------------------------------------------------------------------
    # TAB 1: EXECUTIVE SUMMARY
    # -------------------------------------------------------------------------
    ws_exec = wb.create_sheet(title="Executive Summary")
    ws_exec.views.sheetView[0].showGridLines = True

    ws_exec.cell(row=2, column=2, value="Retail Sales & Customer Analytics - Executive Dashboard").font = title_font

    # KPI Calculation
    tot_rev = df['Revenue'].sum()
    tot_orders = df['Order_ID'].nunique()
    tot_cust = df['Customer_ID'].nunique()
    aov = tot_rev / tot_orders
    top_cat = df.groupby('Product_Category')['Revenue'].sum().idxmax()
    top_prod = df.groupby('Product_Name')['Revenue'].sum().idxmax()

    kpis = [
        ("Total Revenue", f"${tot_rev:,.2f}"),
        ("Total Orders", f"{tot_orders:,}"),
        ("Total Customers", f"{tot_cust:,}"),
        ("Average Order Value", f"${aov:,.2f}"),
        ("Top Category", top_cat),
        ("Top Product", top_prod)
    ]

    # Render KPI Cards (2x3 Grid)
    start_r = 4
    for idx, (title, val) in enumerate(kpis):
        r = start_r + (idx // 3) * 3
        c = 2 + (idx % 3) * 3

        # Merge card header and value cells
        ws_exec.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c+1)
        ws_exec.merge_cells(start_row=r+1, start_column=c, end_row=r+1, end_column=c+1)

        cell_title = ws_exec.cell(row=r, column=c, value=title)
        cell_title.font = Font(name="Calibri", size=10, bold=True, color="595959")
        cell_title.alignment = Alignment(horizontal="center", vertical="center")
        cell_title.fill = kpi_fill

        cell_val = ws_exec.cell(row=r+1, column=c, value=val)
        cell_val.font = kpi_val_font
        cell_val.alignment = Alignment(horizontal="center", vertical="center")
        cell_val.fill = kpi_fill

        for row in ws_exec.iter_rows(min_row=r, max_row=r+1, min_col=c, max_col=c+1):
            for cell in row:
                cell.border = thin_border

    # Section 1: Top 5 Categories Table
    ws_exec.cell(row=12, column=2, value="Category Sales Summary").font = section_font
    cat_df = df.groupby('Product_Category').agg(
        Orders=('Order_ID', 'nunique'),
        Units=('Quantity', 'sum'),
        Revenue=('Revenue', 'sum')
    ).reset_index().sort_values('Revenue', ascending=False)

    cat_headers = ["Product Category", "Total Orders", "Units Sold", "Total Revenue ($)", "% Share"]
    for col_idx, text in enumerate(cat_headers, start=2):
        c = ws_exec.cell(row=13, column=col_idx, value=text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")

    r_idx = 14
    for _, row in cat_df.iterrows():
        ws_exec.cell(row=r_idx, column=2, value=row['Product_Category']).font = regular_font
        ws_exec.cell(row=r_idx, column=3, value=row['Orders']).font = regular_font
        ws_exec.cell(row=r_idx, column=4, value=row['Units']).font = regular_font
        
        c_rev = ws_exec.cell(row=r_idx, column=5, value=row['Revenue'])
        c_rev.font = regular_font
        c_rev.number_format = "$#,##0.00"

        c_share = ws_exec.cell(row=r_idx, column=6, value=row['Revenue'] / tot_rev)
        c_share.font = regular_font
        c_share.number_format = "0.0%"

        for c in range(2, 7):
            ws_exec.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_exec.cell(row=r_idx, column=c).fill = zebra_fill
        r_idx += 1

    # -------------------------------------------------------------------------
    # TAB 2: MONTHLY PERFORMANCE
    # -------------------------------------------------------------------------
    ws_month = wb.create_sheet(title="Monthly Sales Analysis")
    ws_month.views.sheetView[0].showGridLines = True

    ws_month.cell(row=2, column=2, value="Monthly Revenue & Orders Breakdown").font = title_font

    monthly_df = df.groupby('Year_Month').agg(
        Orders=('Order_ID', 'nunique'),
        Units=('Quantity', 'sum'),
        Revenue=('Revenue', 'sum'),
        Profit=('Estimated_Profit', 'sum')
    ).reset_index().sort_values('Year_Month')

    m_headers = ["Year-Month", "Total Orders", "Units Sold", "Total Revenue ($)", "Estimated Profit ($)", "MoM Growth"]
    for col_idx, text in enumerate(m_headers, start=2):
        c = ws_month.cell(row=4, column=col_idx, value=text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")

    prev_rev = None
    r_idx = 5
    for _, row in monthly_df.iterrows():
        ws_month.cell(row=r_idx, column=2, value=row['Year_Month']).font = regular_font
        ws_month.cell(row=r_idx, column=3, value=row['Orders']).font = regular_font
        ws_month.cell(row=r_idx, column=4, value=row['Units']).font = regular_font

        c_rev = ws_month.cell(row=r_idx, column=5, value=row['Revenue'])
        c_rev.font = regular_font
        c_rev.number_format = "$#,##0.00"

        c_prof = ws_month.cell(row=r_idx, column=6, value=row['Profit'])
        c_prof.font = regular_font
        c_prof.number_format = "$#,##0.00"

        mom = (row['Revenue'] - prev_rev) / prev_rev if prev_rev else 0.0
        c_mom = ws_month.cell(row=r_idx, column=7, value=mom if prev_rev else "-")
        c_mom.font = regular_font
        if prev_rev:
            c_mom.number_format = "+0.0%;-0.0%;0.0%"

        prev_rev = row['Revenue']

        for c in range(2, 8):
            ws_month.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_month.cell(row=r_idx, column=c).fill = zebra_fill
        r_idx += 1

    # Total Row
    ws_month.cell(row=r_idx, column=2, value="TOTAL").font = bold_font
    ws_month.cell(row=r_idx, column=3, value=tot_orders).font = bold_font
    ws_month.cell(row=r_idx, column=4, value=df['Quantity'].sum()).font = bold_font
    c_tot_r = ws_month.cell(row=r_idx, column=5, value=tot_rev)
    c_tot_r.font = bold_font
    c_tot_r.number_format = "$#,##0.00"
    c_tot_p = ws_month.cell(row=r_idx, column=6, value=df['Estimated_Profit'].sum())
    c_tot_p.font = bold_font
    c_tot_p.number_format = "$#,##0.00"
    for c in range(2, 8):
        ws_month.cell(row=r_idx, column=c).border = thin_border

    # -------------------------------------------------------------------------
    # TAB 3: PRODUCT & CATEGORY ANALYSIS
    # -------------------------------------------------------------------------
    ws_prod = wb.create_sheet(title="Product Analysis")
    ws_prod.views.sheetView[0].showGridLines = True
    ws_prod.cell(row=2, column=2, value="Top 15 Products by Sales Revenue").font = title_font

    top_prod_df = df.groupby(['Product_ID', 'Product_Name', 'Product_Category']).agg(
        Units=('Quantity', 'sum'),
        Revenue=('Revenue', 'sum'),
        Profit=('Estimated_Profit', 'sum')
    ).reset_index().sort_values('Revenue', ascending=False).head(15)

    p_headers = ["Product ID", "Product Name", "Category", "Units Sold", "Total Revenue ($)", "Est. Profit ($)"]
    for col_idx, text in enumerate(p_headers, start=2):
        c = ws_prod.cell(row=4, column=col_idx, value=text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")

    r_idx = 5
    for _, row in top_prod_df.iterrows():
        ws_prod.cell(row=r_idx, column=2, value=row['Product_ID']).font = regular_font
        ws_prod.cell(row=r_idx, column=3, value=row['Product_Name']).font = regular_font
        ws_prod.cell(row=r_idx, column=4, value=row['Product_Category']).font = regular_font
        ws_prod.cell(row=r_idx, column=5, value=row['Units']).font = regular_font
        
        c_r = ws_prod.cell(row=r_idx, column=6, value=row['Revenue'])
        c_r.font = regular_font
        c_r.number_format = "$#,##0.00"

        c_p = ws_prod.cell(row=r_idx, column=7, value=row['Profit'])
        c_p.font = regular_font
        c_p.number_format = "$#,##0.00"

        for c in range(2, 8):
            ws_prod.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_prod.cell(row=r_idx, column=c).fill = zebra_fill
        r_idx += 1

    # -------------------------------------------------------------------------
    # TAB 4: CUSTOMER ANALYSIS
    # -------------------------------------------------------------------------
    ws_cust = wb.create_sheet(title="Customer Analysis")
    ws_cust.views.sheetView[0].showGridLines = True
    ws_cust.cell(row=2, column=2, value="Customer Segment & Location Analytics").font = title_font

    cust_seg_df = df.groupby('Customer_Segment').agg(
        Customers=('Customer_ID', 'nunique'),
        Revenue=('Revenue', 'sum'),
        Avg_Order=('Revenue', 'mean')
    ).reset_index().sort_values('Revenue', ascending=False)

    cs_headers = ["Customer Segment", "Total Customers", "Total Revenue ($)", "Avg Order ($)"]
    for col_idx, text in enumerate(cs_headers, start=2):
        c = ws_cust.cell(row=4, column=col_idx, value=text)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")

    r_idx = 5
    for _, row in cust_seg_df.iterrows():
        ws_cust.cell(row=r_idx, column=2, value=row['Customer_Segment']).font = regular_font
        ws_cust.cell(row=r_idx, column=3, value=row['Customers']).font = regular_font
        
        c_r = ws_cust.cell(row=r_idx, column=4, value=row['Revenue'])
        c_r.font = regular_font
        c_r.number_format = "$#,##0.00"

        c_a = ws_cust.cell(row=r_idx, column=5, value=row['Avg_Order'])
        c_a.font = regular_font
        c_a.number_format = "$#,##0.00"

        for c in range(2, 6):
            ws_cust.cell(row=r_idx, column=c).border = thin_border
            if r_idx % 2 == 1:
                ws_cust.cell(row=r_idx, column=c).fill = zebra_fill
        r_idx += 1

    # -------------------------------------------------------------------------
    # TAB 5: CLEANED DATA
    # -------------------------------------------------------------------------
    ws_data = wb.create_sheet(title="Cleaned Data")
    ws_data.views.sheetView[0].showGridLines = True

    data_cols = list(df.columns)
    for col_idx, col_name in enumerate(data_cols, start=1):
        c = ws_data.cell(row=1, column=col_idx, value=col_name)
        c.font = header_font
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center")

    for r_idx, row in df.iterrows():
        for c_idx, val in enumerate(row, start=1):
            cell = ws_data.cell(row=r_idx+2, column=c_idx, value=str(val) if pd.api.types.is_datetime64_any_dtype(df.iloc[:, c_idx-1]) else val)
            cell.font = regular_font
            if isinstance(val, float):
                cell.number_format = "0.00"
            cell.border = thin_border

    # Auto-adjust column widths across all worksheets
    for sheet in wb.worksheets:
        for col in sheet.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                if cell.value:
                    val_str = str(cell.value)
                    if len(val_str) > max_len:
                        max_len = len(val_str)
            sheet.column_dimensions[col_letter].width = max(max_len + 4, 12)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"[*] Successfully generated Excel report workbook at: {output_path}")

if __name__ == "__main__":
    build_excel_report()
