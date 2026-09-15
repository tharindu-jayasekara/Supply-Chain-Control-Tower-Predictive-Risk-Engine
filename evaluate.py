import sqlite3
import pandas as pd

db_path = r"D:\Portfolio Projects\Project_1\supply_chain.db"
conn = sqlite3.connect(db_path)

# Check existing tables
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type IN ('table', 'view');", conn)
print("Current tables in DB:\n", tables)

conn.close()