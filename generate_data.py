import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_retail_dataset(num_records=3000, seed=42):
    random.seed(seed)
    np.random.seed(seed)

    # Masters setup
    categories = {
        "Electronics": [
            ("PROD-101", "Wireless Noise-Canceling Headphones", 149.99),
            ("PROD-102", "Smartwatch Fitness Tracker", 199.99),
            ("PROD-103", "4K Ultra HD Monitor 27-inch", 349.99),
            ("PROD-104", "Portable Bluetooth Speaker", 79.99),
            ("PROD-105", "Mechanical Gaming Keyboard", 119.99),
        ],
        "Apparel": [
            ("PROD-201", "Classic Cotton Crewneck T-Shirt", 24.99),
            ("PROD-202", "Slim Fit Denim Jeans", 59.99),
            ("PROD-203", "Lightweight Hooded Sweatshirt", 44.99),
            ("PROD-204", "Breathable Athletic Shorts", 29.99),
            ("PROD-205", "Formal Button-Down Shirt", 49.99),
        ],
        "Home & Kitchen": [
            ("PROD-301", "Digital Air Fryer 5-Quart", 89.99),
            ("PROD-302", "Stainless Steel Cookware Set", 129.99),
            ("PROD-303", "Ergonomic Mesh Office Chair", 189.99),
            ("PROD-304", "Automatic Espresso Coffee Maker", 249.99),
            ("PROD-305", "Robotic Vacuum Cleaner", 299.99),
        ],
        "Beauty & Personal Care": [
            ("PROD-401", "Hydrating Hyaluronic Serum", 34.99),
            ("PROD-402", "Sonic Electric Toothbrush", 69.99),
            ("PROD-403", "Organic Hair Revitalizing Oil", 22.99),
            ("PROD-404", "Gentle Daily Facial Cleanser", 18.99),
            ("PROD-405", "Luxury Shea Butter Lotion", 26.99),
        ],
        "Books & Stationery": [
            ("PROD-501", "Python Data Analytics Blueprint", 39.99),
            ("PROD-502", "Hardcover Bullet Journal & Pen Set", 19.99),
            ("PROD-503", "Financial Freedom Playbook", 27.99),
            ("PROD-504", "Modern UI/UX Design Fundamentals", 32.99),
            ("PROD-505", "World History Illustrated Hardcover", 45.00),
        ],
        "Sports & Outdoors": [
            ("PROD-601", "Non-Slip Yoga Mat 6mm", 29.99),
            ("PROD-602", "Lightweight Trail Running Shoes", 89.99),
            ("PROD-603", "Insulated Water Bottle 32oz", 24.99),
            ("PROD-604", "Adjustable Dumbbell Pair 25lbs", 149.99),
            ("PROD-605", "Waterproof Camping Backpack 40L", 74.99),
        ]
    }

    cities_states = [
        ("Mumbai", "Maharashtra"),
        ("Delhi", "Delhi"),
        ("Bangalore", "Karnataka"),
        ("Hyderabad", "Telangana"),
        ("Chennai", "Tamil Nadu"),
        ("Pune", "Maharashtra"),
        ("Kolkata", "West Bengal"),
        ("Ahmedabad", "Gujarat"),
        ("Jaipur", "Rajasthan"),
        ("Surat", "Gujarat")
    ]

    first_names = [
        "Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Neha", "Rahul", "Sneha",
        "Amit", "Pooja", "Siddharth", "Kavya", "Aditya", "Riya", "Karan", "Shreya",
        "Varun", "Ishita", "Manish", "Divya", "Arjun", "Tanvi", "Sanjay", "Meera",
        "Rajesh", "Nisha", "Gaurav", "Swati", "Deepak", "Anjali"
    ]
    last_names = [
        "Sharma", "Verma", "Patel", "Mehta", "Gupta", "Rao", "Nair", "Singh",
        "Kumar", "Joshi", "Deshmukh", "Reddy", "Chopra", "Malhotra", "Kulkarni",
        "Bhat", "Shah", "Kapoor", "Saxena", "Roy"
    ]

    # Pre-generate 600 unique customers
    num_customers = 600
    customers = []
    for i in range(1, num_customers + 1):
        c_id = f"CUST-{5000 + i}"
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        c_name = f"{fn} {ln}"
        gender = random.choice(["Male", "Female", "Male", "Female", "Other"])
        age = random.randint(18, 68)
        city, state = random.choice(cities_states)
        c_type = random.choice(["New", "Recurring", "VIP", "Recurring"])
        customers.append({
            "Customer_ID": c_id,
            "Customer_Name": c_name,
            "Gender": gender,
            "Age": age,
            "City": city,
            "State": state,
            "Customer_Type": c_type
        })

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_range = (end_date - start_date).days

    payment_modes = ["Credit Card", "Debit Card", "UPI", "Cash on Delivery", "Net Banking"]
    payment_weights = [0.35, 0.20, 0.25, 0.10, 0.10]

    records = []
    order_id_counter = 10001

    for i in range(num_records):
        order_id = f"ORD-{order_id_counter}"
        order_id_counter += 1

        # Pick customer
        cust = random.choice(customers)
        
        # Pick date with seasonal trend (higher sales in Q4)
        rand_days = random.randint(0, days_range)
        o_date = start_date + timedelta(days=rand_days)
        # Boost Q4 dates frequency slightly
        if o_date.month in [10, 11, 12] and random.random() < 0.35:
            rand_days = random.randint(0, days_range)
            o_date = start_date + timedelta(days=rand_days)

        # Format date with occasional string variations
        if random.random() < 0.03:
            date_str = o_date.strftime("%Y/%m/%d")
        elif random.random() < 0.02:
            date_str = o_date.strftime("%d-%m-%Y")
        else:
            date_str = o_date.strftime("%Y-%m-%d")

        # Pick category and product
        cat = random.choice(list(categories.keys()))
        prod_id, prod_name, unit_price = random.choice(categories[cat])

        quantity = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.30, 0.15, 0.07, 0.03])[0]
        discount = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.50, 0.20, 0.15, 0.10, 0.05])[0]
        
        sales = round(quantity * unit_price * (1.0 - discount), 2)
        payment = random.choices(payment_modes, weights=payment_weights)[0]

        # Introduce minor dirty data for cleaning script demonstration
        cust_gender = cust["Gender"]
        cust_age = cust["Age"]
        cust_city = cust["City"]

        # Missing values (~1.5% chance)
        if random.random() < 0.015:
            cust_gender = np.nan
        if random.random() < 0.015:
            cust_age = np.nan
        if random.random() < 0.01:
            payment = np.nan

        # Lowercase string variation (~2% chance)
        if isinstance(cust_gender, str) and random.random() < 0.03:
            cust_gender = cust_gender.lower()

        records.append({
            "Order_ID": order_id,
            "Order_Date": date_str,
            "Customer_ID": cust["Customer_ID"],
            "Customer_Name": cust["Customer_Name"],
            "Gender": cust_gender,
            "Age": cust_age,
            "City": cust_city,
            "State": cust["State"],
            "Product_ID": prod_id,
            "Product_Category": cat,
            "Product_Name": prod_name,
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Discount": discount,
            "Sales": sales,
            "Payment_Mode": payment,
            "Customer_Type": cust["Customer_Type"]
        })

    # Add ~25 exact duplicate rows to test duplicate handling
    duplicates = random.sample(records, 25)
    records.extend(duplicates)
    random.shuffle(records)

    df = pd.DataFrame(records)
    
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/retail_sales_raw.csv", index=False)
    print(f"Generated raw dataset with {len(df)} rows at data/raw/retail_sales_raw.csv")

if __name__ == "__main__":
    generate_retail_dataset()
