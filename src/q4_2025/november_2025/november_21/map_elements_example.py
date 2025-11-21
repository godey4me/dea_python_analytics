import math
import polars as pl

df = pl.DataFrame({
    "values": [10, 7, 1, 23]
})

def my_log(x):
    return math.log(x)

# Apply UDF to each element
result = df.with_columns(
    pl.col("values")
      .map_elements(my_log, return_dtype=pl.Float64)
      .alias("log_value")
)

print(result)