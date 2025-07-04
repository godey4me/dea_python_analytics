## DuckDB

### Description

- In-memory or file-based database that can operate with Python to handle SQL-related workflows very efficiently.

- Provides interoperability with various data processing libraries in Python including `pandas`.

### Installation and Setup

- Install `DuckDB` via `PyPi`.

```bash
pip install duckdb
```

### Basic Usage - Setup a Connection

```python
from os import getcwd
from duckdb import connect

# Path to where you will save the database
db_path = getcwd() + "/path/to/database.db"

# Setup a connection to the database
cursor = connect(database=db_path)
```

### Basic Usage - Read CSV Files into Tables

- `...` indicates a continuation from the previous section.

```python
...

# URL to some public data 
csv_url = "https://ashfaq-nsclc-dataset.s3.us-east-1.amazonaws.com/ali_datasets/Electric_Vehicle_Population_Data.csv"

# Write your SQL query
query = f'''

    SELECT *
    FROM read_csv_auto("{csv_url}")
    LIMIT 100

'''

# Execute SQL using the .sql() method from the cursor
result = cursor.sql(query=query)

print(result)
```

### Basic Usage - Convert Table Results into DataFrames

```python
...

# Convert the result into a DataFrame
df = result.df()

# Get information about the pandas DataFrame
df.info()
```

### Basic Usage - Persist the Table

- `table_name` could be:
    - An actual table that exists inside DuckDB
    - Pandas DataFrame
    - function that auto infers data from another format
        - `.csv` : `read_csv_auto()`
        - `.parquet` : `read_parquet_auto()`

```python
...

cursor.sql(
    query = """

        CREATE OR REPLACE TABLE table_name AS (

            SELECT *
            FROM table_name

        )

    """
)
```

### Basic Usage - Leveraging Pandas to Persist the Data

```python
...

# Use the .to_sql() method from pandas to save tables into the DuckDb database
df.to_sql(name='table_name', 
    con=cursor, 
    index=False, 
    if_exists='replace')

```

### Basic Usage - Filter the Data

```python
...
# Assumption - The table is already in DuckDB
query = """
    SELECT *
    FROM table
    WHERE ...
    LIMIT ...
"""

result = cursor.sql(query=query)

print(result)

# DataFrame
df = result.df()

df.info()
```

