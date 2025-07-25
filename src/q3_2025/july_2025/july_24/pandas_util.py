import pandas as pd
from typing import Any

# Helper Function - identify_dtype
def identify_dtype(frame: pd.DataFrame, col: str) -> tuple[Any, type]:
    """
    ## Inputs
    - frame (pandas DataFrame): The original DataFrame
    - col (string) : The column to apply the data type investigation

    ## Output
    - value_dtype (type): The actual data type of the first value of a specific column in the DataFrame
    """

    # First value that belongs to a column in a DataFrame
    first_value = frame.iloc[0][col]

    value_dtype = type(first_value)

    return first_value, value_dtype



# Helper Function
def clean_explode(frame: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    ## Inputs
    - frame (pandas DataFrame): The original DataFrame with columns that contain list values.
    - col (string) : Column to explode on.

    ## Output
    - clean_frame (pandas DataFrame): This DataFrame will explode and also combine the new values into a singular Dataframe.
    """

    # Explode on the column
    frame = frame.explode(column=col).reset_index().drop('index', axis=1)

    # The column to explode on as a Series
    col_as_a_series = frame[col].to_list()

    col_df = pd.json_normalize(data=col_as_a_series).reset_index().drop('index', axis=1)

    # Rename the columns of the column DataFrame
    col_df.columns = [f'{col}_{internal_col}' for internal_col in col_df.columns.tolist()]

    # Concatenate them
    clean_frame = pd.concat(objs=[frame, col_df], axis=1)

    return clean_frame



def get_final_normalized_frame(data: list[dict]) -> pd.DataFrame:
    """
    ## Inputs
    - data (list of dictionaries) : Input data which will become a DataFrame in pandas.

    ## Output
    - frame (pandas DataFrame)
    """

    # Originally, normalize the DataFrame
    df = pd.json_normalize(data=data)

    # Columns that have the list data type
    cols_with_list_type = []

    for col in df.columns.tolist():
        value, col_dtype = identify_dtype(frame=df, col=col)

        print(f"Column {col} has dtype: {col_dtype}")

        if isinstance(value, list):
            # Add the column if the value happens to be a list
            cols_with_list_type.append(col)
    
    # Explode the columns that need it
    first_col_to_explode = cols_with_list_type[0]

    merged_df = clean_explode(frame=df, col=first_col_to_explode)

    merged_df.drop(first_col_to_explode, axis=1, inplace=True)

    # If you have more than one column to explode
    if len(cols_with_list_type) > 1:
        # Iterate through the rest of the columns
        for col in cols_with_list_type[1:]:
            merged_df = clean_explode(merged_df,col)

            # Drop the exploded column
            merged_df.drop(col, axis=1, inplace=True)
    

    return merged_df