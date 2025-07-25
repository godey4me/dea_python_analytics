import pandas as pd
from pandas_util import get_final_normalized_frame, identify_dtype
from sample_data import json_data

# # Normalize the original DataFrame
# normalized_df = pd.json_normalize(data=json_data)

# result = identify_dtype(frame=normalized_df, col='orders')

# print(result)

result = get_final_normalized_frame(data=json_data)

print(result)