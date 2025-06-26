import pandas as pd
from dagster import Definitions, job, op, resource, Field
from sqlalchemy import create_engine

@resource(config_schema={"postgres_url": Field(str)})
def pg_db(context):
    return create_engine(context.resource_config["postgres_url"])

@op(required_resource_keys={"pg_db"})
def extract_table(context) -> pd.DataFrame:
    return pd.read_sql_table("your_table", con=context.resources.pg_db)

@op
def transform_column(df):
    df["name"] = df["name"].str.upper()
    return df

@op
def write_csv(df):
    df.to_csv("output.csv", index=False)

@job(resource_defs={"pg_db": pg_db})
def postgres_to_csv_job():
    write_csv(transform_column(extract_table()))

defs = Definitions(jobs=[postgres_to_csv_job])