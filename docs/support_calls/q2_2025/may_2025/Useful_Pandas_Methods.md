## 🐼 Mastering pandas groupby, crosstab, and melt

### 📚 Introduction

- `pandas` is a powerful Python library for data analysis. Three of its most useful tools for summarizing and reshaping data are `groupby`, `crosstab`, and `melt`. Understanding how to use these functions effectively can greatly enhance your data analysis capabilities.

---

### 🔹 groupby: Grouping and Aggregating Data

#### 🔧 Syntax

```python
DataFrame.groupby(by=None, axis=0, level=None, as_index=True, sort=True, group_keys=True, observed=False, dropna=True)
```

#### 🧪 Example: Sales Data

Let’s create a synthetic dataset representing sales transactions:

```python
import pandas as pd

# Sample sales data
data = {
    'Region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West'],
    'Product': ['A', 'A', 'B', 'B', 'A', 'B', 'A', 'B'],
    'Sales': [250, 150, 200, 300, 400, 120, 330, 500]
}

df = pd.DataFrame(data)
print(df)
```

Output: ￼

  Region Product  Sales
0  North       A    250
1  South       A    150
2   East       B    200
3   West       B    300
4  North       A    400
5  South       B    120
6   East       A    330
7   West       B    500


#### 📊 Grouping by Region

```python
# Total sales by region
region_sales = df.groupby('Region')['Sales'].sum()
print(region_sales)
```

Output:

Region
East     530
North    650
South    270
West     800
Name: Sales, dtype: int64

#### 📈 Grouping by Region and Product

```python
# Total sales by region and product
region_product_sales = df.groupby(['Region', 'Product'])['Sales'].sum()
print(region_product_sales)
```

Output: ￼

Region  Product
East    A          330
        B          200
North   A          650
South   A          150
        B          120
West    B          800
Name: Sales, dtype: int64


#### 📌 Common Aggregation Functions
- `.sum()` – Total sum
- `.mean()` – Average
- `.count()` – Count of non-NA/null entries
- `.min()` / `.max()` – Minimum / Maximum
- `.agg()` – Multiple aggregations ￼ ￼

```python
# Multiple aggregations
aggregated = df.groupby('Product')['Sales'].agg(['sum', 'mean', 'count'])
print(aggregated)
```
Output:

         sum        mean  count
Product                        
A         830  276.666667      3
B        1120  280.000000      4



---

### 🔹 crosstab: Cross-Tabulation of Categorical Data

#### 🔧 Syntax

```python
pd.crosstab(index, columns, values=None, rownames=None, colnames=None, aggfunc=None, margins=False, margins_name='All', dropna=True, normalize=False)
```

#### 🧪 Example: Customer Preferences

- Let’s create a synthetic dataset representing customer preferences:

```python
# Sample customer data
data = {
    'Gender': ['Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Male', 'Female'],
    'Preference': ['Tea', 'Coffee', 'Tea', 'Coffee', 'Tea', 'Tea', 'Coffee', 'Coffee']
}

df = pd.DataFrame(data)
print(df)
```

Output: ￼

  Gender Preference
0   Male        Tea
1 Female     Coffee
2 Female        Tea
3   Male     Coffee
4 Female        Tea
5   Male        Tea
6   Male     Coffee
7 Female     Coffee

#### 📊 Basic Crosstab

```python
# Frequency table of Gender vs Preference
ct = pd.crosstab(df['Gender'], df['Preference'])
print(ct)
```

Output: ￼

Preference  Coffee  Tea
Gender                
Female           2    2
Male             2    2

#### 📈 Crosstab with Aggregation

- Suppose we have scores associated with each entry:

```python
# Adding scores to the dataset
df['Score'] = [85, 90, 88, 75, 95, 80, 70, 92]
print(df)
```

Output:

  Gender Preference  Score
0   Male        Tea     85
1 Female     Coffee     90
2 Female        Tea     88
3   Male     Coffee     75
4 Female        Tea     95
5   Male        Tea     80
6   Male     Coffee     70
7 Female     Coffee     92

```python
# Average score by Gender and Preference
ct_avg = pd.crosstab(df['Gender'], df['Preference'], values=df['Score'], aggfunc='mean')
print(ct_avg)
```

Output:

Preference  Coffee   Tea
Gender                 
Female        91.0  91.5
Male          72.5  82.5

#### 📌 Adding Margins and Normalization

```python
# Crosstab with totals and normalized values
ct_norm = pd.crosstab(df['Gender'], df['Preference'], margins=True, normalize='index')
print(ct_norm)
```

Output:

Preference  Coffee  Tea  All
Gender                      
Female         0.5  0.5  1.0
Male           0.5  0.5  1.0
All            0.5  0.5  1.0


---

### 🔹 melt: Reshaping Data from Wide to Long Format

#### 🔧 Syntax

```python
pd.melt(frame, id_vars=None, value_vars=None, var_name=None, value_name='value', col_level=None, ignore_index=True)
```

#### 🧪 Example: Student Scores

- Let’s create a synthetic dataset representing student scores:

```python
# Sample student data
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Math': [85, 90, 78],
    'Science': [88, 92, 84],
    'History': [82, 85, 80]
}

df = pd.DataFrame(data)
print(df)
```

Output:

      Name  Math  Science  History
0    Alice    85       88       82
1      Bob    90       92       85
2  Charlie    78       84       80

#### 📊 Melting the DataFrame

```python
# Reshaping from wide to long format
melted_df = pd.melt(df, id_vars=['Name'], var_name='Subject', value_name='Score')
print(melted_df)
```

Output: ￼

      Name  Subject  Score
0    Alice     Math     85
1      Bob     Math     90
2  Charlie     Math     78
3    Alice  Science     88
4      Bob  Science     92
5  Charlie  Science     84
6    Alice  History     82
7      Bob  History     85
8  Charlie  History     80

#### 📌 Customizing Column Names

```python
# Customizing the variable and value column names
melted_df = pd.melt(df, id_vars=['Name'], var_name='Subject', value_name='Score')
print(melted_df)
```

Output:

      Name  Subject  Score
0    Alice     Math     85
1      Bob     Math     90
2  Charlie     Math     78
3    Alice  Science     88
4      Bob  Science     92
5  Charlie  Science     84
6    Alice 