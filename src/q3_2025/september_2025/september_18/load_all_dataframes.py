import pandas as pd
from os import getcwd, listdir

# Data Path
data_path = getcwd() + "/data/csv_files/sample_dataframes"

# List of DataFrames
df_list = [pd.read_csv(f'{data_path}/{file}') for file in listdir(data_path)]

# concatenate 
df = pd.concat(objs=df_list)


df.info()
