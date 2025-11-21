import polars as pl
from os import getcwd

# Read a CSV file
csv_path = getcwd() + "/data/csv_files/smart_home_energy_usage_dataset.csv"

# Read the CSV as a DataFrame
df = pl.read_csv(source=csv_path)

print(df)

# Schema
print(df.schema)

# Columns
cols = df.columns

pandas_cols = df.to_pandas().columns.to_list()

# LazyFrame
df = pl.scan_csv(source=csv_path)

print(df)

# Physical DataFrame
df = df.collect()

print(df)

# # .sql()
# df = df.sql(query="SELECT * FROM df WHERE day_of_week = 'Tuesday'",
#             table_name='df')

print(df)

# SQLContext
ctx = pl.SQLContext(frames={'energy_usage': df})

result = ctx.execute(query="SELECT home_id, season FROM energy_usage", 
                     eager=True)

df = result

print(df)