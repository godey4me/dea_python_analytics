import pandas as pd
from pandas_util import normalized_frame
from sample_data import json_data
from format_util import line_separator

df = normalized_frame(data=json_data)

df.info()

print(df.head())

example_type = type(df['orders'].iloc[0])

print(example_type)

df = df.explode(column='orders')

print(df)

orders_series = df['orders']

print("Series: ", orders_series)

line_separator()

# Individual row
print("individual row in Series:", orders_series.iloc[0])

line_separator()

# Break it out into list of dictionaries
list_of_dicts = df['orders'].to_list()

print("List of dictionaries across rows: ", list_of_dicts)

line_separator()

new_df = pd.json_normalize(data=list_of_dicts).reset_index().drop('index', axis=1)

print(df.head())

line_separator()

print(new_df.head())

result = pd.concat(objs=[df.reset_index().drop('index', axis=1), new_df], axis=1)

result.drop('orders', axis=1, inplace=True)

print(result)


