import pandas as pd

def normalize_json(data: list[dict]) -> pd.DataFrame:
    df = pd.json_normalize(data)

    def recursively_flatten(df: pd.DataFrame) -> pd.DataFrame:
        while True:
            # Track columns to flatten/explode
            nested_cols = []
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, (dict, list))).any():
                    nested_cols.append(col)

            if not nested_cols:
                break

            for col in nested_cols:
                # If column is list of dicts → explode and normalize
                if df[col].apply(lambda x: isinstance(x, list)).any():
                    df = df.explode(col).reset_index(drop=True)

                # If column is dict → normalize and join
                if df[col].apply(lambda x: isinstance(x, dict)).any():
                    new_cols = pd.json_normalize(df[col].dropna()).add_prefix(f"{col}.")
                    df = df.drop(columns=[col]).reset_index(drop=True)
                    df = pd.concat([df, new_cols], axis=1)

        return df

    return recursively_flatten(df)