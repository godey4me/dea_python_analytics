import pandas as pd
from os import getcwd

# DataFrame from scratch
df_dict = {'col_one' : [1,2,3,4,5],
           'col_two' : [6,7,8,9,10]}

print(type(df_dict))

df = pd.DataFrame.from_dict(df_dict)

print(type(df))

print(df)

# Select rows and columns

## Selecting rows
first_row = df.iloc[0]

print(first_row)
print(type(first_row))

# Name of the series?
print(first_row.dtype)

# .values
row_values = first_row.values
print(row_values)
print(type(row_values))

# .index
row_index = first_row.index

print(row_index)
print(type(row_index))

# Values
print(row_index.values)
print(type(row_index.values))

# Information about your DataFrame
df.info()

# Summary Statistics
print(df.describe())

def print_describe(df: pd.DataFrame) -> None:

    print(df.describe())

print_describe(df)

# .loc
descriptive_stats = df.describe()

print(descriptive_stats.iloc[1])

# Export the data to a CSV file
descriptive_stats.to_csv('my_data.csv')

print(getcwd())

# Read data
csv_path = getcwd() + "/data/csv_files/International_Education_Costs.csv"

# New Variable
df = pd.read_csv(csv_path)

print(type(df))

df.info()

print(df)

# .apply
df['Visa_Fee_USD'] = df['Visa_Fee_USD'].apply(lambda x: 1.35 * x)

print(df)