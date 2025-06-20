import os
import pandas as pd
from dagster import job, op, resource, Field, StringSource
from sqlalchemy import create_engine

# 1. Define a DB connection resource
# Resources are decorators
## Contains a parameter called config_schema
@resource(config_schema={"postgres_url" : Field(StringSource, description="PostgreSQL connection")})
def postgresql_db(context):
    return create_engine(context.resource_config["postgres_url"])

# 2. Read data from the DB into a DataFrame
# op is a decorator
## Contains a parameter called required_resource_keys
## Used to enforce prerequisites for the operation
@op(required_resource_keys={"postgresql_db"})
def extract_table(context) -> pd.DataFrame:
    # Get the engine
    engine = context.resources.postgresql_db

    try:
        # Get the DataFrame
        df = pd.read_sql_table(table_name="hospital_readmissions_json", schema='dea', con=engine)

        # Add a log statement
        context.log.info(f"Loaded {len(df)} rows from the table.")
    
    except Exception as e:
        # Add a log statement that mentions the exception
        context.log.error(f"Exception occurred: {e}")

    return df

# 3. Transform a column in the DataFrame
@op
def transformation(df: pd.DataFrame) -> pd.DataFrame:
    # Get the first row from raw_json column
    row = df.iloc[0]['raw_json']

    # Transform the row into a DataFrame
    transformed_df = pd.json_normalize([row])

    # Perform a transpose
    transformed_df = transformed_df.T

    # Reset the index and drop the extra index column
    transformed_df.reset_index(inplace=True)

    # Rename the columns
    transformed_df.columns = ['tag', 'value']

    return transformed_df

# 4. Export DataFrame to CSV
@op
def write_to_csv(df: pd.DataFrame):
    # Define the output path
    output_path = os.getcwd() + "/output.csv"

    # Export the DataFrame to a CSV
    df.to_csv(output_path, index=False)

    print(f"Wrote transformed data to {output_path}.")

# 5. Define the job
# job is a decorator
## resource_defs is a parameter of the decorator
@job(resource_defs={"postgresql_db" : postgresql_db})
def postgres_to_csv_job():
    # Use the internal functions of operations in here
    df = extract_table()

    transformed_df = transformation(df)

    write_to_csv(transformed_df)