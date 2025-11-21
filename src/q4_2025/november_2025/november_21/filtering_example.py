import polars as pl

data = {
    'col_1' : [1,2,3,4,5],
    'col_2' : [6,7,8,9,10]
}

df = pl.DataFrame(data)

# Get the values from column 1 that are greater than 3
result_df = df.filter(pl.col('col_1') > 3)

print(result_df)

# Compound filtering
result_df = df.filter(
    (pl.col('col_1') > 3) & (pl.col('col_2') < 10)
)

print(result_df)

# Is In Example
country_list = ['usa', 'uae']

data = {
    'col_1' : ['charlie', 'chaplin', 'heineken'],
    'col_2' : ['usa', 'uae', 'de']
}

df = pl.DataFrame(data)

# Use .is_in()
result_df = df.filter(pl.col('col_2').is_in(country_list))

print(result_df)