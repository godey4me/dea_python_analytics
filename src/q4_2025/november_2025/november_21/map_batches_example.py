import polars as pl

df3 = pl.DataFrame({
    "values_1": [1, 2, 3],
    "values_2": [10, 20, 30]
})

# UDF is at the Series level
def add_columns(arr1: pl.Series, arr2: pl.Series) -> pl.Series:
    return arr1**2 + arr2**2

out = df3.with_columns(
    # Build a struct first
    pl.struct(["values_1", "values_2"])
      .map_batches( # Apply map_batches with a lambda to refer to the struct
         lambda s: add_columns(s.struct.field("values_1"),  s.struct.field("values_2")),
         return_dtype=pl.Int64
      )
      .alias("sum_vals")
)

print(out)