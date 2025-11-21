import polars as pl

# DataFrame
sample_dict = {
    'col_1': list(range(1, 11)),
    'col_2' : list(range(11, 21))
}

df = pl.DataFrame(data=sample_dict)

print(df)

# Convert to a pandas DataFrame
pandas_df = df.to_pandas()

print(pandas_df)

# Convert back into polars
df = pl.DataFrame._from_pandas(data=pandas_df)

print(df)