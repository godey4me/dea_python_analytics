import pandas as pd
from ydata_profiling import ProfileReport

# Create a DataFrame
frame_dict = {
    'col_1': list(range(10)),
    'col_2': list(range(10, 20))
}

df = pd.DataFrame.from_dict(frame_dict)

# Generate a report
report = ProfileReport(df=df)

# to_file() method to export the report into a HTML file
report.to_file('report.html')