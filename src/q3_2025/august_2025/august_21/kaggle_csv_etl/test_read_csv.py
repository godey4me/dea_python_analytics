import pytest
import pandas as pd
from os import getcwd

# pytest.fixture
@pytest.fixture
def csv_df():

    # Relative Paths
    data_path = getcwd() + "/data/csv_files/smart_home_energy_usage_dataset.csv"

    print(data_path)

    # Read the data to become a pandas DataFrame
    df = pd.read_csv(data_path)

    return df

# Unit Test Case #1 - Ensuring we got all the rows
def test_num_rows(csv_df):
    assert csv_df.shape[0] == 100000

def test_num_cols(csv_df):
    assert csv_df.shape[1] == 9