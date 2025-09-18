from pandas import concat, DataFrame

# Creating two DataFrames
df = DataFrame({f'col_{j}': [f'name_{i}' for i in range(1, 101)] for j in range(1, 11)})

df.info()

# Random Sample of our above DataFrame
df_sample = df.sample(n=50)

# Stack the DataFrames on each other
concatenated_df = concat(objs=[df, df_sample], axis=1).fillna(value=0)

# Info
concatenated_df.info()

print("Before: ")
print(df.head())
print(df_sample.head())

print('-'*100)

print("After: ")
print(f"Head: {concatenated_df.head()} \n\n\n Tail: {concatenated_df.tail()}")