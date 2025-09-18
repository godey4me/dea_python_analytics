from os import getcwd
from pandas import concat, DataFrame
from typing import Literal

# Import the decorator
from profiler_decorator import profile_data

@profile_data
def transformation(n_rows: int = 100, 
                   n_cols: int = 20, 
                   sample_size: int = 50, 
                   axis_choice: Literal[0, 1] = 0) -> DataFrame:

    # Creating two DataFrames
    df = DataFrame({f'col_{j}': [f'name_{i}' for i in range(1, n_rows + 1)] for j in range(1, n_cols + 1)})

    df.info()

    # Random Sample of our above DataFrame
    df_sample = df.sample(n=sample_size)

    # Stack the DataFrames on each other
    concatenated_df = concat(objs=[df, df_sample], axis=axis_choice)

    # Info
    concatenated_df.info()

    print("Before: ")
    print(df.head())
    print(df_sample.head())

    print('-'*100)

    print("After: ")
    print(f"Head: {concatenated_df.head()} \n\n\n Tail: {concatenated_df.tail()}")

    return concatenated_df

# Running the Function
result = transformation(n_rows=10000, n_cols=30, sample_size=5000)

# Info
result.info()

# List of DataFrames - Comprehension
df_list = [result.sample(n=3000) for i in range(5)]

# Loop through the list and export the DataFrames as CSV files
data_path = getcwd() + "/data/csv_files/sample_dataframes"

for i, elem in enumerate(df_list):
    elem.to_csv(path_or_buf=f'{data_path}/sample_{i+1}.csv', index=False)