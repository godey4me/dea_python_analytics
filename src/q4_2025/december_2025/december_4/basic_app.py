import polars as pl
from os import getcwd
from fastapi import FastAPI
from uvicorn import run

# Path to the CSV file
csv_path = getcwd() + "/data/csv_files/fastapi_examples/gym_members_dataset.csv"

# Generate the polars DataFrame
df = pl.read_csv(source=csv_path)

json_records = df.to_dict(as_series=False)

# Application object
app = FastAPI()

# Routes
@app.get(path='/')
def starting_page():
    return "Welcome to the web app."

@app.get(path='/entry')
def entry():
    return "Greeting"

@app.get(path='/example_json')
def json_response():
    return {
        'message' : 'This is a test.'
    }

@app.get(path='/kaggle_data')
def kaggle_data():

    # Convert the polars DAtaFrame into a pandas DataFrame
    pandas_df = df.to_pandas()

    # Drop missing values
    pandas_df = pandas_df.dropna().reset_index().drop('index', axis=1)

    # JSON records
    json_records = [pandas_df.iloc[i].to_dict() for i in range(pandas_df.shape[0])]

    return json_records

# Run function
run(app=app, host='0.0.0.0', port=8080)