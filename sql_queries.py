import sqlite3
import pandas as pd

conn = sqlite3.connect("sales.db")

# Query 1
query1 = "SELECT SUM(Weekly_Sales) AS total_sales FROM sales"
print(pd.read_sql(query1, conn))

# Query 2
query2 = """
SELECT Store, SUM(Weekly_Sales) AS total
FROM sales
GROUP BY Store
ORDER BY total DESC
LIMIT 5
"""
print(pd.read_sql(query2, conn))

# Query 3
query3 = """
SELECT strftime('%Y-%m', Date) AS month,
SUM(Weekly_Sales) AS total
FROM sales
GROUP BY month
"""
print(pd.read_sql(query3, conn))

conn.close()