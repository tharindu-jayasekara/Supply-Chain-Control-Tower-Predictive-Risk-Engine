import sqlite3
import pandas as pd

# Load raw CSV into Pandas
csv_path = r'D:\Portfolio Projects\Project_1\DataCoSupplyChainDataset.csv'
print("Loading CSV into Pandas...")
df = pd.read_csv(csv_path, encoding='iso-8859-1')

# Create a local SQLite database file
conn = sqlite3.connect(r"D:\Portfolio Projects\Project_1\supply_chain.db")

# Write DataFrame into SQLite table
print("Writing data to SQLite database...")
df.to_sql('orders', conn, if_exists='replace', index=False)

conn.close()
print("Database created successfully as 'supply_chain.db'!")

