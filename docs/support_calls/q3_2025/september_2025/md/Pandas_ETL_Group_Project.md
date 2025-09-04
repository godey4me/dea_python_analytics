## Pandas ETL Group Project

### Education Statistics - Pandas ETL - Level 1

1. Download this [dataset](https://www.kaggle.com/datasets/theworldbank/education-statistics?utm_source=chatgpt.com) from Kaggle.

2. Think about a business or operational problem that requires some analysis of the data and write down an approach which would involve data cleaning.

3. Write the Python code to perform your transformations.

4. Add unit testing with PyTest wherever suitable.

5. Export your final transformed data into individual tables in a `DuckDB` database called `education_statistics.db`.

- Bonus Points (PyTest):

1. Add at least two fixtures.
2. Add at least one parametrized set of inputs to test.

### Education Statistics - Pandas ETL - Level 2

1. Same as above, but the entire workflow is orchestrated via `Dagster`.

- Bonus Points (Dagster)

1. Use the `dagster-ui` to view the materialized workflow post-completion.