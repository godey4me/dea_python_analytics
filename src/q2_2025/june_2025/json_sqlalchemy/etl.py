import pandas as pd
from os import getcwd
from sqlalchemy.types import JSON

# Custom Modules
from json_transformation import json_transform
from sqlalchemy_util import postgresql_connection

# Data Path
data_path = getcwd() + "/data/csv_files/taco_sales_(2024-2025).csv"

# Load the data as a DataFrame
df = pd.read_csv(filepath_or_buffer=data_path)

df.info()

print("DataFrame loaded from CSV file.")

# Transform the DataFrame into a JSON-like DataFrame
new_df = json_transform(df=df)

new_df.info()

print("DataFrame transformed into a JSON-like DataFrame.")

# Establish a PostgreSQL Connection
cursor = postgresql_connection()

# Mapping of raw_json to the corresponding SQLAlchemy JSON Type
dtype_mapping = {
    'raw_json' : JSON
}

# Save the DataFrame as a new table within the PostgreSQL database
new_df.to_sql(
    name='taco_sales',
    con=cursor,
    index=False,
    if_exists='replace',
    dtype=dtype_mapping
)

print("Table has been loaded into PostgreSQL.")
