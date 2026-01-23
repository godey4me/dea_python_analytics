import pandas as pd
from requests import get

# Helper Functions
def retrieve_df_from_url(url: str) -> pd.DataFrame:
    """
    ## Retrieving DataFrame from URL
    
    ### Inputs
    - url (string): URL to perform a HTTP GET request towards.

    ### Output
    - df (pandas.core.dataframe) : Pandas DataFrame representation of the JSON data after performing a URL request.
    
    
    ### Description
    - This function will take a JSON response from a URL and transform it into a pandas DataFrame representation.
    """


    # HTTP GET Request
    response = get(url=url)

    try:
        # JSON
        result = response.json()
    except Exception as e:
        raise ValueError(f"Exception occurred: {e}")
    
    # Normalize JSON
    df = pd.json_normalize(result)

    return df