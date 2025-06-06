import pandas as pd

# Custom module
from sqlalchemy_util import postgresql_connection

# Establish the connection
cursor = postgresql_connection()

# .read_sql_table() from pandas
df = pd.read_sql_table(table_name='taco_sales', con=cursor, schema='public')

# .info()
df.info()

# .head()
print(df.head())

# First row and inspect the data type
first_json_value = df.iloc[0]['raw_json']

print(type(first_json_value))

# Get the raw_json as a Series
raw_json_series = df['raw_json']

# Transform the series into a list
raw_json_as_list = raw_json_series.to_list()

# JSON Normalize to create a DataFrame
new_df = pd.json_normalize(data=raw_json_as_list)

new_df.info()

print(new_df.head())