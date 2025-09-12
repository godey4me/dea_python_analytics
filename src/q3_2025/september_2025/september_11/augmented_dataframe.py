import pandas as pd
from ydata_profiling import ProfileReport

# Inherit from the DataFrame
class AugmentedDataFrame(pd.DataFrame):
    # Constructor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # Create Profile
    def create_profile(self, file_path: str) -> ProfileReport:
        
        # Report
        self.report = ProfileReport(df=self)

        # Export to a file
        self.report.to_file(output_file=file_path)

        return self.report