import requests
import pandas as pd
from os import getcwd, environ
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pymongo import MongoClient

# Path to .env file
env_path = getcwd() + "/src/q2_2025/may_2025/may_15/.env"

# Load environment variables
load_dotenv(dotenv_path=env_path)

# URL
url = "https://jsonplaceholder.typicode.com/posts"

# Make HTTP GET Request
response = requests.get(url=url)

# Get JSON from the response
json_response = response.json()

# Create Mongo client
mongo_host = environ.get('MONGO_HOST')
mongo_user = environ.get('MONGO_USER')
mongo_password = environ.get('MONGO_PASSWORD')
mongo_port = environ.get('MONGO_PORT')
mongo_db = environ.get('MONGO_DB')

# Create a URL
mongo_url = f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/{mongo_db}'

# Mongo Client
mongo_client = MongoClient(host=mongo_url)

# Switch to the database api_results
mongo_database = mongo_client['api_results']

# Switch to a collection name of your choice
mongo_collection = mongo_database['posts_api_data']

# Insert the data from the JSON response into the collection with .insert_many()
mongo_collection.insert_many(documents=json_response)

print("Data has been inserted into Mongo collection.")

# Retrieve the data from MongoDB using .find()
mongo_results = mongo_collection.find()

# Convert to a list from a MongoDB Cursor
mongo_results = list(mongo_results)

# Normalize into a pandas DataFrame
df = pd.json_normalize(data=mongo_results)

print("Generated DataFrame from Mongo results.")

# Get the information
df.info()

# Set up a PostgreSQL connection
postgres_host = environ.get('POSTGRES_HOST')
postgres_user = environ.get('POSTGRES_USER')
postgres_password = environ.get('POSTGRES_PASSWORD')
postgres_port = environ.get('POSTGRES_PORT')
postgres_db = environ.get('POSTGRES_DB')

# Setup the URL
postgres_url = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'

# Create an engine
engine = create_engine(url=postgres_url)

# Setup a connection via SQLAlchemy via .connect()
cursor = engine.connect()

# Transform the _oid Series into a string in the DataFrame
## use .astype()
df_columns = df.columns.tolist()

oid_col = df_columns[0]

df[oid_col] = df[oid_col].astype(dtype=str)

# Create a schema
schema_name = "rishov_test"

schema_query = f"""
    CREATE SCHEMA IF NOT EXISTS {schema_name}
"""

# Use text() to get the executable logic for cursor.execute()
schema_query = text(text=schema_query)

# Use the SQLAlchemy connection to execute the query
## 1. .execute()
## 2. .commit()
cursor.execute(statement=schema_query)
cursor.commit()

# Load the DataFrame as a table within the schema
df.to_sql(name='posts_api_results', 
          con=cursor, 
          schema=schema_name,
          if_exists='replace',
          index=False
          )

print("Table loaded into PostgreSQL.")
