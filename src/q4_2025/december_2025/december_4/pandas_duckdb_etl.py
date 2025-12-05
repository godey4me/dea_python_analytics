import polars as pl
from os import getcwd
from duckdb import connect

# DuckdB Path
duckdb_path = getcwd() + "/data/duckdb/fastapi_examples/simple_kaggle_app.db"

# Path to the CSV file
csv_path = getcwd() + "/data/csv_files/fastapi_examples/gym_members_dataset.csv"

# Generate the polars DataFrame
df = pl.read_csv(source=csv_path)

# Remove the missing values
df = df.drop_nulls().to_pandas()

df.columns = [col.lower() for col in df.columns]

# Save the DataFrame as a table
cursor = connect(database=duckdb_path)

# Query
sql_query = """

DROP TABLE gym_membership_churn;

CREATE TABLE gym_membership_churn AS (
    SELECT *
    FROM df
);

"""

# Execute the query
result = cursor.sql(query=sql_query)

# Reading from the new table
result = cursor.sql(query='SELECT * FROM gym_membership_churn')

print(result)

# Convert the record set back into a pandas or polars DataFrame
pandas_df = result.df()

pandas_df.info()

# Close your DuckDB connection
cursor.close()


