from os import getcwd, environ
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection

env_path = getcwd() + "/.env"

# Load environment variables
load_dotenv(dotenv_path=env_path)

# Function to establish the connection
def postgres_connect(host: str = None, user: str = None, password: str = None, db_name: str = None, port: int = None) -> Connection:

    # Get the credentials from the env vars
    postgres_host = environ.get('POSTGRES_HOST')
    postgres_user = environ.get('POSTGRES_USER')
    postgres_password = environ.get('POSTGRES_PASSWORD')
    postgres_port = environ.get('POSTGRES_PORT')
    postgres_db = environ.get('POSTGRES_DB')

    print(postgres_port)

    if db_name is None:
        db_name = postgres_db
    
    if port is None:
        port = postgres_port

    if host is None:
        host = postgres_host
    
    if user is None:
        user = postgres_user
    
    if password is None:
        password = postgres_password

    
    
    # URL
    url = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    # Engine
    engine: Engine = create_engine(url=url)

    # return the connection
    return engine.connect()
