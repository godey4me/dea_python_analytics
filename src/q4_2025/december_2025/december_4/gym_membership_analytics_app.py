from os import getcwd
from duckdb import connect
from fastapi import FastAPI
from uvicorn import run

# DuckdB Path
duckdb_path = getcwd() + "/data/duckdb/fastapi_examples/simple_kaggle_app.db"

# App
app = FastAPI()

# Routes
@app.get(path='/churn_by_membership_type')
def churn_by_membership_type():

    # Connection
    cursor = connect(database=duckdb_path)

    # Query
    query = """

    SELECT
        membership_type,
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS num_churns
    FROM gym_membership_churn
    GROUP BY
        membership_type
    ORDER BY
        num_churns DESC

    """

    # .sql() method
    result = cursor.sql(query=query)

    # JSON conversion
    result = result.df()

    json_records = [result.iloc[i] for i in range(result.shape[0])]

    # Close the DuckDB connection
    cursor.close()

    return json_records


run(app=app, host='0.0.0.0', port=8080)