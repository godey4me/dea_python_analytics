import pandas as pd
from test_framework_exercise import test_tracker

# Random DataFrame
random_df = pd.DataFrame.from_dict({
    'col_one' : list(range(10))
})

random_df.info()

# Function
@test_tracker
def check_row_count(df: pd.DataFrame):

    # Get number of rows
    number_rows = df.shape[0]

    # Assert statement
    assert number_rows == 10

@test_tracker
def check_column_count(df: pd.DataFrame):

    # Get number of columns
    number_cols = df.shape[1]

    assert number_cols == 2



if __name__ == "__main__":
    # Execute the functions
    pass_count, total_tests = check_row_count(random_df)
    pass_count, total_tests = check_column_count(random_df)

    # Print Statement
    print(f"{pass_count}/{total_tests} tests passed.")