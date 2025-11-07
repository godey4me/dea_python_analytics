from dotenv import load_dotenv
from os import getcwd, environ
from sqlalchemy import create_engine

# Path to the .env file
env_path = getcwd() + "/src/q4_2025/november_2025/november_6/postgres.env"

load_dotenv(dotenv_path=env_path)

# Credentials
host = environ.get('POSTGRES_HOST')
user = environ.get('POSTGRES_USER')
password = environ.get('POSTGRES_PASSWORD')
port = environ.get('POSTGRES_PORT')
database = environ.get('POSTGRES_DATABASE')

connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'

# Engine
engine = create_engine(url=connection_string)

