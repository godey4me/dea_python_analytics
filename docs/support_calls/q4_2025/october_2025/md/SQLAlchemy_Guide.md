## Guide to SQLAlchemy

### Description

- `SQLAlchemy` is a package that creates a bridge between a SQL server and Python.

- It uses a `dialect` which is a specific type of driver that allows you to specify which particular SQL server SQLAlchemy has to build a bridge with so Python can understand.

### Main Dialects

1. PostgreSQL

- Uses a driver called `psycopg2` 

2. Microsoft SQL

- Uses a driver called `pymssql`

3. MySQL

- Uses a driver called `pymysql`

### Installation and Setup

1. Install the following packages:

- requirements.txt

```txt
pandas
sqlalchemy
psycopg2-binary
```

```bash
pip install -r requirements.txt
```

### Example - Connect to PostgreSQL


- Basics of a connection string

```txt
postgresql://username:password@ip_address:port/database
```

- Insecure Python example

```python
username = ''
password = ''
host = ''
port = ''
database = ''

connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
```

- Secure Python example

1. Load all the different components as environment variables.

- Create a file called `.env`

```.env
POSTGRES_USER="something"
POSTGRES_PASSWORD="something"
POSTGRES_HOST="something"
POSTGRES_PORT="something"
POSTGRES_DATABASE="something"
```

- Install the `python-dotenv` package so you can load your environment variables.

```bash
pip install python-dotenv
```

```python
from os import getcwd, environ
from dotenv import load_dotenv

env_path = getcwd() + "/.env"

# Load environment variables
load_dotenv(env_path)

# Credentials
host = environ.get('POSTGRES_HOST')
user = environ.get('POSTGRES_USER')
password = environ.get('POSTGRES_PASSWORD')
port = environ.get('POSTGRES_PORT')
database = environ.get('POSTGRES_DATABASE')

connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
```

#### Build the Connection

```python
from sqlalchemy import create_engine

# Variable
engine = create_engine(connection_string)

# Turn the engine into a Connection
cursor = engine.connect()

# Do whatever you want with the cursor
```

#### Read Data into Pandas

```python
import pandas as pd

# Create a table output as a DataFrame
df = pd.read_sql_table('users', con=cursor, schema='public')

# Results of the DataFrame
df.info()

# SQL Query Results
query = """

SELECT *
FROM schema.table_name
WHERE col_name = 'Active'

"""

df = pd.read_sql_query(query=query, con=cursor)
```
