import pandas as pd

# Custom modules
from postgres_connection import postgres_connect

# Get the connection
cursor = postgres_connect(port=8070)

print(type(cursor))