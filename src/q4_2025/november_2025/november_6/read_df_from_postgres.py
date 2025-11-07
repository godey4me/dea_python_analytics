import pandas as pd
from postgres_connection import engine

# Connection
cursor = engine.connect()

df = pd.read_sql_table(table_name='users', con=cursor)

df.info()

print(df)
