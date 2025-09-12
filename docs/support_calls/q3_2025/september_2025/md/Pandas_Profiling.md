## Pandas Profiling

### Description

- Pandas profiling which is now referred to as `ydata_profiling` is a framework that allows you to develop an interactive HTML dashboard that covers all the insights from your pandas DataFrames.

#### Insights

1. Missing Value Analysis
2. Descriptive Statistics
3. Correlations between Columns
4. Text Column Insights
    - Character Count
    - Word Count
    - Frequency Analysis
5. Memory Consumption
6. Alerts
    - High Cardinality
    - Presence of Zeros
    - Highly Correlated

### Setup and Installation

1. Install `ydata_profiling` via `pip`

```bash
pip install ydata-profiling
```

### Basic Usage

1. Generate a Profile Report.

```python
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
```

2. Export the report to a HTML file.

- `...` is a continuation from the previous example.

```python
...

# to_file() method to export the report into a HTML file
report.to_file('report.html')
```