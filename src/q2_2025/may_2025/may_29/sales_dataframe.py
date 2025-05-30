import pandas as pd

# Sample sales data
data = {
    'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West'],
    'Product': ['A', 'A', 'B', 'B', 'A', 'B', 'A', 'B'],
    'Sales': [250, 150, 200, 300, 400, 120, 330, 500]
}

df = pd.DataFrame(data)
print(df)