import pandas as pd

def normalized_frame(data: list[dict]) -> pd.DataFrame:

    # First DataFrame
    df = pd.json_normalize(data=data)

    cols_with_list_row = []

    # Check if any of my columns have a list type in the first row
    for col in df.columns.tolist():
        # First row from each column
        first_value = df[col].iloc[0]

        first_value_type = type(first_value)

        if isinstance(first_value_type, list):
            cols_with_list_row.append(col)
    
    # Go through the cols with list row
    if len(cols_with_list_row) > 0:
        # Explode the columns one by one
        for col in cols_with_list_row:
            new_df = df.explode(column=col)

            col_list_dicts = new_df[col].to_list()

            new_normalized_df = pd.json_normalize(data=col_list_dicts)

            df = pd.concat(objs=[new_df, new_normalized_df], axis=1)
    
    return df