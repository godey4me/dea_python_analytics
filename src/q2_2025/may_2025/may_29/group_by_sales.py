import pandas as pd

# Sample sales data
data = {
    'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West'],
    'Product': ['A', 'A', 'B', 'B', 'A', 'B', 'A', 'B'],
    'Sales': [250, 150, 200, 300, 400, 120, 330, 500]
}

df = pd.DataFrame(data)
print(df)

region_sales = df.groupby('Region')['Sales'].sum()
print(region_sales)

# Get the index
print(region_sales.index)

# Change the index to a column - reset_index()
region_sales_df = region_sales.reset_index()

print(region_sales_df)

transposed_region_sales = region_sales_df.T

print(transposed_region_sales.index)

print(transposed_region_sales.columns)

transposed_region_sales.columns = transposed_region_sales.loc['Region'].tolist()

print(transposed_region_sales)