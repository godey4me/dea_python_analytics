from os import getcwd
from duckdb import connect

# Path to where you will save the database
db_path = getcwd() + "/data/duckdb/sample.db"

# Setup a connection to the database
cursor = connect(database=db_path)

# URL to some public data 
csv_url = "https://ashfaq-nsclc-dataset.s3.us-east-1.amazonaws.com/ali_datasets/Electric_Vehicle_Population_Data.csv"

# Write your SQL query
query = f'''
        SELECT *
        FROM read_csv_auto("{csv_url}")
        LIMIT 2000
'''

# Execute SQL using the .sql() method from the cursor
result = cursor.sql(query=query)

print(result)

# Convert the data into a pandas DataFrame
df = result.df()

# Seeing the information
df.info()

# Column Preprocessing
columns = df.columns.tolist()

columns = [elem.lower().replace(' ', '_').replace('-', '_').replace('(', '').replace(')','') 
           for elem in columns]

print(columns)

# Rename the columns
df.columns = columns

df.drop('city', axis=1, inplace=True)

print(df.columns)

df.info()

print(df.head())

df.to_sql(name='ev_data_v3', con=cursor, index=False, if_exists='replace')

print("Saved the ev_data_v3 table to the DuckDB database.")

# # Transform the DataFrame into a new table
# result = cursor.sql(
    
#     query=f'''

#         CREATE OR REPLACE TABLE ev_data_v2 AS (
#             SELECT *
#             FROM {df}
            
#         )

#     '''
# )

# print(result)

# Read from the table
new_df = cursor.sql(query='SELECT * FROM ev_data_v3').df()

new_df.info()



