import pandas as pd
import polars as pl
from os import getcwd
from datetime import datetime

def calculate_time(func):
    def closure(*args, **kwargs):
        start = datetime.now()

        result = func(*args, **kwargs)

        end = datetime.now()

        # Difference
        delta = end - start

        print("Total seconds elapsed: ", delta.total_seconds())

        return result
    
    return closure

csv_path = getcwd() + "/data/csv_files/user_top_artists.csv"

@calculate_time
def load_large_frame():

    df = pd.read_csv(csv_path)

    return df

# df = load_large_frame()

@calculate_time
def load_polars_frame():

    df = pl.read_csv(csv_path)

    return df

df = load_polars_frame()

first_five_rows = df[0:5]

print(type(first_five_rows))

print(first_five_rows)

# Convert polars into pandas
df = df.to_pandas()

# In-Memory SQL Table
with pl.SQLContext(frames={'users': df}) as context:

    # Query
    query = "SELECT * FROM users WHERE playcount > 3000"

    result = context.execute(query=query, eager=True)

    print(result)
