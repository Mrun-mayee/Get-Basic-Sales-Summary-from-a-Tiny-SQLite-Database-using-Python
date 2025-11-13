# 🧮 TASK 7: Basic Sales Summary from SQLite Database

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Step 1: Connect to the Database
# -------------------------------
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# -------------------------------
# Step 2: Create Sample Table (if not exists)
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
);
""")

# Insert data only if table is empty
cursor.execute("SELECT COUNT(*) FROM sales;")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("Laptop", 5, 70000),
        ("Mouse", 20, 500),
        ("Keyboard", 10, 1500),
        ("Monitor", 7, 12000),
        ("Headphones", 15, 2000)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?);", sample_data)
    conn.commit()

# -------------------------------
# Step 3: Run SQL Queries
# -------------------------------
# Total quantity and revenue
cursor.execute("SELECT SUM(quantity), SUM(quantity * price) FROM sales;")
total_qty, total_revenue = cursor.fetchone()

# Product-wise summary
query = """
SELECT product, SUM(quantity) AS total_quantity, 
       SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product;
"""
df = pd.read_sql_query(query, conn)

# -------------------------------
# Step 4: Display Output
# -------------------------------
print("=== 🧾 SALES SUMMARY ===")
print(f"Total Quantity Sold: {total_qty}")
print(f"Total Revenue: ₹{total_revenue:,.2f}\n")

print("=== 📦 PRODUCT-WISE SALES ===")
print(df)

# -------------------------------
# Step 5: Bar Chart Visualization
# -------------------------------
plt.bar(df["product"], df["total_revenue"])
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------------
# Step 6: Close Connection
# -------------------------------
conn.close()
