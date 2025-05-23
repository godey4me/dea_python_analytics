## YData Profiling

### Description

- `ydata_profiling` (formerly known as pandas-profiling) is a powerful Python library that automates Exploratory Data Analysis (EDA) by generating detailed reports from a pandas DataFrame. 

- These reports provide insights into:
    - data types
    - missing values
    - distributions
    - correlations

### Setup and Installation

- Install via `pip`

```bash
pip install ydata-profiling
```

### Basic Usage

```python
import pandas as pd
from ydata_profiling import ProfileReport

# Load your dataset
df = pd.read_csv("your_dataset.csv")

# Create a ProfileReport
profile = ProfileReport(df, title="Profiling Report")

# Or save the report as an HTML file
profile.to_file("profiling_report.html")
```

### Resources

- [ydata-profiling Documentation](https://docs.profiling.ydata.ai/latest/)

