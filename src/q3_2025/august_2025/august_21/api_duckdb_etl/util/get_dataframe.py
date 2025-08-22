import pandas as pd
from util.retrieve_api_response import get_posts


# Function
def get_df(resp: list[dict]) -> pd.DataFrame:

    # Use json_normalize()
    df = pd.json_normalize(data=resp)

    return df