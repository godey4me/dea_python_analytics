import pytest
import pandas as pd
from util.retrieve_api_response import get_posts
from util.get_dataframe import get_df

# Create a fixture
@pytest.fixture
def resp_frame() -> pd.DataFrame:
    # Get API response in deserialized Python objects (JSON source)
    resp = get_posts()

    # Get DataFrame
    return get_df(resp=resp)

# Create a test with the fixture as input
def test_row_count(resp_frame):
    assert resp_frame.shape[0] == 100

