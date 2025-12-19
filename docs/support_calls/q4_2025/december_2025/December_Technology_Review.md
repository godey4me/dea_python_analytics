## December Technology Review

### Agenda

1. Pandas
2. Polars
3. DuckDB
4. Basic Routing with FastAPI

### Pandas

- Manipulate data that looks like tables (if you come from SQL), but within Python.

#### Structures

- DataFrame
    - Made up of the other two (series and index)
    - Rows and columns
    - Looks like a table, but represented in Python
    - Allows you to choose columns and rows for manipulating data.
- Series
    - Row or a column
    - Properties
        - data type
        - name
        - Index (specific index values that refer to each element in the whole collection)
- Index
    - Used as an identifier for specific elements in the Series or DataFrame.
    - By default, it is numbers that start from 0.

