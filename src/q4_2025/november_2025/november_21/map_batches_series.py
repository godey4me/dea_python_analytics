import math
import polars as pl

df = pl.DataFrame({
    "keys": ["a","a","b","b"],
    "values": [10, 7, 1, 23]
})

def diff_from_mean(series: pl.Series) -> pl.Series:
    total = series.sum()
    mean = total / len(series)
    return series - mean

result = df.select(
    pl.col("values").map_batches(diff_from_mean, return_dtype=pl.Float64)
)

print(result)


# One liner
result = df.select(pl.col('values').map_elements(lambda s: math.log(s), pl.Float32))

print(result)