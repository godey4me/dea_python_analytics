import pandas as pd

# Custom modules
from postgres_connection import postgres_connect

# Get the connection
cursor = postgres_connect()

print(type(cursor))

query = "SELECT * FROM dea.student_scores LIMIT 30"

df = pd.read_sql_query(sql=query, con=cursor)

df.info()