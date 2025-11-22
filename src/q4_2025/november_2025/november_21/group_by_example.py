import numpy as np
import polars as pl
import hvplot.polars
import matplotlib.pyplot as plt

col_2_values = np.random.randint(low=10, high=1000, size=10)


data = {
    'col1' : [np.random.randint(low=1, high=3, size=1)[0] for i in range(10)],
    'value' : col_2_values,
    'other_col' : col_2_values * 3
}

df = pl.DataFrame(data)

print(df)

result = df.group_by(
    by="col1"               # or list of cols or expressions
    , maintain_order=True   # optional: preserve input row order per group
).agg(
    pl.col("value").sum().alias("value_sum"),
    pl.col("other_col").mean().alias("other_mean"),
    # another expression
)

print(type(result))

print(result)

# Visualize the bar chart
chart = result.hvplot.bar(x='by', y='value_sum')

plt.show()