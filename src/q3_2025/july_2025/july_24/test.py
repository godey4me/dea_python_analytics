import pandas as pd
from pandas_util import get_final_normalized_frame, identify_dtype
from sample_data import json_data

result = get_final_normalized_frame(data=json_data)

print(result)