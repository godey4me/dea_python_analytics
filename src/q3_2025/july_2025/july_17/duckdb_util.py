import pandas as pd
from duckdb import DuckDBPyConnection

def load_frame_to_duckdb(cursor: DuckDBPyConnection, 
                         table_name: str,
                         frame: pd.DataFrame
                        ) -> None:
    
    cursor.sql(query=f"""
            CREATE OR REPLACE TABLE {table_name} AS (

               SELECT *
            FROM frame   
            
            )  
    """)


def view_duckdb_table(cursor: DuckDBPyConnection, table_name: str) -> pd.DataFrame:

    return cursor.sql(query=f"SELECT * FROM {table_name}").df()
