## Working with JSON via SQLAlchemy

### Description

- This guide will help you understand how to work with JSON data with pandas and SQLAlchemy.

### Installation and Setup

- Python Modules
    - `pandas`
    - `sqlalchemy`
    - `psycopg2-binary`
    - `python-dotenv`

### Basic Usage - Using the SQLAlchemy JSON Type

```python
from sqlalchemy.types import SQLAlchemyJSON

# Assume you have a Pandas DataFrame with JSON column
df = ...

# Assume you have a SQLAlchemy connection
cursor = ...

# Create a mapping
dtype_mapping = {'json_col' : SQLAlchemyJSON}

# Use .to_sql()
df.to_sql(
    name='table_name',
    con=cursor,
    index=False,
    if_exists='replace',
    dtype=dtype_mapping
)
```

### Basic Usage - Transforming DataFrames into JSON Format

```python
# Assume you have a DataFrame
df = ...

# Use .to_dict() and ensure the
## `orient` parameter is set to `records`
df_as_json = df.to_dict(orient='records')

# Create a new DataFrame
new_df = pd.DataFrame()

# Get a new Series in the DataFrame
new_df['raw_json'] = df_as_json

# Follow steps from previous 
## block to save as a new table
new_df.to_sql(
    ...
)
```