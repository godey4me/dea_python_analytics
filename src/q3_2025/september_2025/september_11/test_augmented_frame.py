import pandas as pd
from augmented_dataframe import AugmentedDataFrame

frame_dict = {
    'col_1' : list(range(10)),
    'col_2' : list(range(10, 20))
}

aug_frame = AugmentedDataFrame.from_dict(data=frame_dict)

# Info
aug_frame.info()

# Describe
print(aug_frame.describe())

# Profile
aug_frame.create_profile(file_path='report.html')