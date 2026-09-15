import sqlite3
import pandas as pd
import numpy as np

# Step 1: Establish Connection to SQLite
db_path = r"D:\Portfolio Projects\Project_1\supply_chain.db"
conn = sqlite3.connect(db_path)

print("Fetching raw data from SQLite...")

df = pd.read_sql_query("SELECT * FROM orders", conn)
print(df.head())
# Step 2: Clean Column Names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
)

# Step 3: Datetime Parsing
datetime_cols = ["order_date_dateorders", "shipping_date_dateorders"]
for col in datetime_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Step 4: Feature Engineering
# Calculate actual delay relative to scheduled shipping days
if "days_for_shipping_real" in df.columns and "days_for_shipment_scheduled" in df.columns:
    df["shipping_delay_days"] = df["days_for_shipping_real"] - df["days_for_shipment_scheduled"]

# Define Target Variable for ML Model: 1 = Late, 0 = On Time / Early
if "late_delivery_risk" in df.columns:
    df["is_delayed"] = df["late_delivery_risk"].astype(int)
else:
    df["is_delayed"] = (df["shipping_delay_days"] > 0).astype(int)

# Step 5: Handle Missing Values (Pandas 2.x & 3.0 Compatible)

# Explicitly select both 'object' and 'str' to handle text columns cleanly
categorical_cols = df.select_dtypes(include=["object", "str"]).columns
df[categorical_cols] = df[categorical_cols].fillna("Unknown")

# Select numeric columns explicitly
numeric_cols = df.select_dtypes(include=["number"]).columns
df[numeric_cols] = df[numeric_cols].fillna(0)

# Step 6: Write Cleaned Data Back to SQLite as a New Table
clean_table_name = "cleaned_supply_chain"
df.to_sql(clean_table_name, conn, if_exists="replace", index=False)

print(f"Data Cleaning Complete. Cleaned records saved to table: '{clean_table_name}'")
conn.close()