## Streamlit and FastAPI Interaction

### Key Mechanism

- On one server, you launch your Streamlit app.
- On another server, you launch your FastAPI app.

- Use `requests` library to make a request to the `FastAPI` app to get a JSON response which can then be parsed / rendered into the Streamlit application.

### Best Practices

1. Within `Streamlit`, use `@st.cache_data()` decorator to cache any already completed HTTP requests to the FastAPI app within Streamlit.

2. **Persistent Cache**: Build a DuckDB database that stores the data responses and just loads directly from DuckDB and have the database connection as a cached resource with `@st.cache_resource()`.

