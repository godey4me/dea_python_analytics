import pandas as pd
from ydata_profiling import ProfileReport

def profile_data(func):
    # Closure
    def closure(*args, **kwargs):

        # Execute the function input
        result: pd.DataFrame = func(*args, **kwargs)

        ## Assumption - You end up getting a pandas DataFrame
        report = ProfileReport(df=result, explorative=True)

        # Generate the profile
        report.to_file(output_file=f'{func.__name__}.html')

        return result
    
    return closure