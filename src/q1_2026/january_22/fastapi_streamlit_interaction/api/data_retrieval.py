import pandas as pd
from os import getcwd

# Data Path
data_path = getcwd() + "/data"

# Heart Disease data
heart_dataset = f'{data_path}/Heart_Disease_Prediction.csv'
student_dataset = f'{data_path}/StudentPerformance.csv'

# DataFrames
heart_df = pd.read_csv(heart_dataset)
student_df = pd.read_csv(student_dataset)

# Transform the DataFrames into JSON-like representations
heart_data_array = [heart_df.iloc[i].to_dict() for i in range(heart_df.shape[0])]
student_data_array = [student_df.iloc[i].to_dict() for i in range(student_df.shape[0])]

