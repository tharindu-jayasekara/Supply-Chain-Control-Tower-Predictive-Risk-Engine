import sqlite3
import pandas as pd
import os

# Uses the current working directory of your VS Code terminal
DB_PATH = os.path.join(os.getcwd(), 'supply_chain.db')
print(f"Database path: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)

query = 'SELECT Market, COUNT(*) FROM orders GROUP BY Market ORDER BY COUNT(*) DESC;'
df = pd.read_sql_query(query, conn)
conn.close()

print(df)
