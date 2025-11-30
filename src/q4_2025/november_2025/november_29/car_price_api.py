import pandas as pd
from fastapi import FastAPI

# Data Path
data_path = 'car_price_dataset_medium.csv'

# App
app = FastAPI()

# Transformation
df = pd.read_csv(data_path)

# Transform every row into a dictionary
df_as_json = [df.iloc[i].to_dict() for i in range(df.shape[0])]

# GET endpoint
@app.get(path='/car_price')
def car_price():
    return df_as_json