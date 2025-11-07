import pandas as pd
from os import getcwd

# Custom Modules or Objects
from retrieve_data_from_web import data

# JSON Normalization
## Keys and Values -> Columns and Rows
df = pd.json_normalize(data=data)

df.info()

print(df.head(10))

df_v2 = pd.DataFrame(data=data)

df_v2.info()

print(df_v2.head(10))

print(pd.__version__)

# Export our DataFrame into a .parquet file
parquet_path = getcwd() + "/data/parquet"

df.to_parquet(path=f'{parquet_path}/photos_api_response.parquet', compression='snappy', index=False)

