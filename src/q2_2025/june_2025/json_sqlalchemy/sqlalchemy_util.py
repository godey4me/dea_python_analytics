from os import getcwd, environ
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Optional Imports
from sqlalchemy.engine import Engine, Connection

# Get a path to the .env file
env_path = getcwd() + "/.env"

# Load environment variables
load_dotenv(dotenv_path=env_path)

host = environ.get('POSTGRES_HOST')
user = environ.get('POSTGRES_USER')
password = environ.get('POSTGRES_PASSWORD')
port = environ.get('POSTGRES_PORT')




# Function to connect to PostgreSQL
def postgresql_connection(db: str = None) -> Connection:

    if db is None:

        # Grab the database from environment variables
        db = environ.get('POSTGRES_DB')

    # Connection String
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db}'

    # Creating an engine object
    engine: Engine = create_engine(url=connection_string)

    # Create a connection
    cursor = engine.connect()

    return cursor