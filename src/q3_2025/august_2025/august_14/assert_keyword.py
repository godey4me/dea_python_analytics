import pandas as pd

# Dictionary
data_dict = {
    'column_one': list(range(1, 6)),
    'column_two': list(range(6, 11))
}

# DataFrame in pandas
df = pd.DataFrame.from_dict(data=data_dict)



# Assert Number of Rows is Matching with 5
assert df.shape[0] == 5