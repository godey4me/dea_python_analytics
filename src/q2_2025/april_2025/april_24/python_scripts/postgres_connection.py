from os import getcwd, environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection

# Load environment variables
load_dotenv(dotenv_path=getcwd() + "/.env")

# Function to establish the connection
def postgres_connect(db_name: str = None, port: int = 5432) -> Connection:

    # Get the credentials from the env vars
    host = environ.get('POSTGRES_HOST')
    user = environ.get('POSTGRES_USER')
    password = environ.get('POSTGRES_PASSWORD')
    postgres_port = environ.get('POSTGRES_PORT')
    db = environ.get('POSTGRES_DB')

    print(postgres_port)

    if db_name is None:
        db_name = db
    
    if port is None:
        port = postgres_port
    
    # URL
    url = f'postgresql://{user}:{password}@{host}:{port}/{db}'

    # Engine
    engine: Engine = create_engine(url=url)

    # return the connection
    return engine.connect()
