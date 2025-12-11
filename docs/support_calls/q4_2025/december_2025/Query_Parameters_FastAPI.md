## Query Parameters in FastAPI

### Description

- Input parameters that can be used to customize the HTTP request for REST APIs.
    - Often identified by using a `?` and then the name of a parameter.

```python
# arg is a query parameter with a value of 3
url = "https://some_api.com?arg=3"
```

### Mechanisms in FastAPI

- Parameters to the function being decorated at route-level.

```python
@app.get("/some_route")
def get_info(
    arg_one: int,
    arg_two: int = 10,
    arg_three: str | None = None
):
    return locals()
```

- `Query` class to provide validations.

```python
from fastapi import Query

@app.get("/some_route")
def get_info(
    arg_one: int = Query(description="First argument", ge=1, le=100),
    arg_two: int = Query(description="Second argument", ge=1, le=20, value=10),
    arg_three: str | None = Query(description="Third argument", value=None)
):
    return locals()
```