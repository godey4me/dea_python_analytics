## Pydantic Response Models and Pagination in FastAPI

### Pydantic Response Models

- FastAPI can use `BaseModel` classes from Pydantic to create a schema for how the JSON response should be generated for a route.

- Usually defined in a file such as `models.py` for a generic app.

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    id: int
    name: str
    value: float

class PaginatedItems(BaseModel):
    items: List[Item]
    total: int
    page: int
    page_size: int
```

- The chosen model is then what gets returned by the route in a FastAPI application.

```python
@app.get('/some_route', response_model=PaginatedItems)
def some_route():
    return PaginatedItems(
        items=[],
        total=0,
        page=1,
        page_size=50
    )
```

### Pagination

#### Strategy 1 - Use Offset and Limit with Database

- The route will have the following Query parameters:
    - `page` : Number of the page
    - `page_size` : Number of items in a page

- Calculate an offset by using the formula:

$$ \text{offset} = (\text{page} - 1) \cdot \text{page size} $$

- Get your SQL query to use `LIMIT` being the page size and `OFFSET` to your calculated offset.

```sql
SELECT *
FROM table
LIMIT page_size OFFSET offset
```

- Worked out example:

```python
@app.get("/items", response_model=PaginatedItems)
def list_items(
    page: int = Query(1, ge=1, description="Page number (starting at 1)"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page"),
    db = Depends(get_db),
):
    """
    Paginated list of items from DuckDB.
    """
    # Convert page/page_size -> offset/limit
    offset = (page - 1) * page_size

    # Get total count
    total = db.execute("SELECT COUNT(*) FROM items").fetchone()[0]

    if total == 0:
        return PaginatedItems(
            items=[],
            total=0,
            page=page,
            page_size=page_size,
        )

    # Guard against requesting pages beyond the end (optional)
    if offset >= total:
        raise HTTPException(status_code=404, detail="Page out of range")

    # Fetch current page
    rows = db.execute(
        """
        SELECT id, name, value
        FROM items
        ORDER BY id
        LIMIT ? OFFSET ?
        """,
        [page_size, offset],
    ).fetchall()

    items = [Item(id=r[0], name=r[1], value=r[2]) for r in rows]

    return PaginatedItems(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
    )
```

### Strategy 2 - In-Memory Pagination at Route

- Assume your route has the objects in-memory (perhaps as a list).

- Use offset and page_size to create start and end indices to slice the list.

$$ \text{end idx} = \text{offset} + \text{page size} $$

- Worked out example

```python
FAKE_ITEMS = [
    Item(id=i, name=f"Item {i}", value=float(i))
    for i in range(1, 501)
]

@app.get("/local-items", response_model=PaginatedItems)
def list_local_items(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """
    Paginated list of items from an in-memory list.
    """
    total = len(FAKE_ITEMS)
    offset = (page - 1) * page_size
    end = offset + page_size

    if offset >= total:
        # You can also choose to return an empty list instead of 404
        raise HTTPException(status_code=404, detail="Page out of range")

    # Slice the Python list
    page_items = FAKE_ITEMS[offset:end]

    return PaginatedItems(
        items=page_items,
        total=total,
        page=page,
        page_size=page_size,
    )
```