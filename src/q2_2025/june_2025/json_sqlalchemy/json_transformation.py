import pandas as pd


def json_transform(df: pd.DataFrame, json_col: str = 'raw_json') -> pd.DataFrame:
    """
    ### Inputs
    - df (pandas DataFrame) - Input DataFrame that does not have any JSON data.

    ### Optional Inputs
    - json_col (string): Name of the column that will contain the JSON data in your output DataFrame.

    ### Output
    - new_df (pandas DataFrame) - DataFrame output that contains one column with JSON data.
    """

    # Transform the input DataFrame into a JSON-like representation
    df_as_json = df.to_dict(orient='records')

    # Create a new DataFrame
    new_df = pd.DataFrame()

    new_df[json_col] = df_as_json

    return new_df