import polars as pl
from os import getcwd
from simple_base_model import User

# Data Path to the CSV file
csv_path = getcwd() + "/data/csv_files/users_example.csv"

df = pl.read_csv(csv_path).to_pandas()

print(df)

records = [df.iloc[i].to_dict() for i in range(df.shape[0])]

print(records)

records = [User(**record) for record in records]

# Dump
records = [record.model_dump() for record in records]

record_df = pl.json_normalize(records)

print(record_df)

# Generate 2 users
users = [
    {'name' : 'x' , 'age' : 40, 'email_id': 'john_doe@gmail.com'},
    {'name' : 'y', 'age': 64, 'email_id': 'y@hotmail.com'}
]

users = [User(**user) for user in users]

users = [u.model_dump() for u in users]

print(users)

# Create the polars DataFrame
df = pl.json_normalize(data=users)

print(df)