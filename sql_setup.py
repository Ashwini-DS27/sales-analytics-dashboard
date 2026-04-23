import sqlite3
import pandas as pd

# Create database
conn = sqlite3.connect("sales.db")

# Load CSV
df = pd.read_csv("sales.csv")

# Insert into database
df.to_sql("sales", conn, if_exists="replace", index=False)

print("✅ Data inserted into database successfully!")

conn.close()