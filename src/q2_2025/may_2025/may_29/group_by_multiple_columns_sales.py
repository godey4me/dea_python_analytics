import pandas as pd

from sales_dataframe import df

df_copy: pd.DataFrame = df.copy()


# Total sales by region and product
region_product_sales = df_copy.groupby(['Region', 'Product'])['Sales'].sum()
print(region_product_sales)

region_product_sales_index = region_product_sales.index

print(region_product_sales_index)

# Reset index
region_product_df = region_product_sales.reset_index()

print(region_product_df)

# Go through each region and then sum the sales

# Group by 

# # Export to the CSV
# region_product_df.to_csv(index=False)