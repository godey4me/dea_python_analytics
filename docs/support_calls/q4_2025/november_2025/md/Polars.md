## Polars - Parallel Data Processing in Python without Spark

### Description

- Polars is a new and performant data processing module that originated in Rust and was ported to Python.
- Its design is modeled after pandas with majority of pandas-related classes and methods being identical.

### Key Differences

- Polars can use multiple cores to process data whereas pandas handles everything as a single process.
- Contains an interface that is compliant to users who come from:
    - Pandas
    - Spark

### Setup and Installation

- You can install `polars` via `pip`.

```bash
pip install polars
```

### Basic Usage - Creating a DataFrame

- Classes in `polars` are modeled after `pandas`.
    - Index
    - Series
    - DataFrame

- DataFrames can either be:
    - Entirely materialized DataFrames
    - LazyFrames
        - Resulting from data scans where the data itself doesn't persist (generator-like behavior)
        - Builds a query plan, defers execution, and allows optimizations before it becomes a final DataFrame loaded in-memory.

```python
import polars as pl

df = pl.DataFrame({
    "id" : [1,2,3,4],
    "value" : [10, 20, 30, 40]
})
```

- Read or scan from a CSV

```python
...

csv_file = 'example.csv'

# Fully materialized DataFrame
df = pl.read_csv(csv_file)

# LazyFrame
df = pl.scan_csv(csv_file)
```

- Supports various formats similar to pandas
    - Excel
    - Parquet
    - JSON
    ...

#### SQL Context

- `.sql()` method

```python
...

# self is the name of the DataFrame as a SQL table
filtered = df.sql("SELECT id, value FROM self WHERE value >= 30")
print(filtered)
```

- `SQLContext` class
    - Key in the `frames` dictionary represents name of the table when executing SQL query on the DataFrame.


```python
ctx = pl.SQLContext(frames={"main" : df})

# DataFrame
result = ctx.execute(
    """
    SELECT
        id, (value * 2) as value_squared
    FROM main
    WHERE id % 2 = 0
    """,
    eager=True
)

print(result)
```