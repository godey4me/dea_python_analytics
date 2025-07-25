from os import getcwd
from duckdb import connect
from sample_data import json_data
from pandas_util import normalize_json
from duckdb_util import load_frame_to_duckdb, view_duckdb_table

# Database path
db_path = getcwd() + "/data/duckdb/sample_exercise.db"

cursor = connect(database=db_path)

# Normalize sample data
df = normalize_json(data=json_data)

df.columns = [col.replace('.', "_") for col in df.columns.tolist()]

# Load into DuckDB database
load_frame_to_duckdb(cursor=cursor, table_name='raw_data', frame=df)

# View the table
result = view_duckdb_table(cursor=cursor, table_name='raw_data')

result.info()

print(result)


# Create new table
cursor.sql(query="""
    CREATE OR REPLACE TABLE clean_data AS (
        SELECT 
            DISTINCT user_id,
            user_name,
           user_address_city,
           user_address_zip,
           orders_id,
           orders_item       
        FROM raw_data
    )
""")

# Get final result
result = view_duckdb_table(cursor=cursor, table_name='clean_data')

result.info()

print(result)