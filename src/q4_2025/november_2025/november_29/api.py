from duckdb import connect, DuckDBPyConnection
from typing import Optional
from os import getcwd
from fastapi import FastAPI, Depends, HTTPException, Query, status

# Custom imports
from pydantic_models import Product, ProductCreate, PaginatedProducts

DB_PATH = getcwd() + "/data/duckdb/example.duckdb"

app = FastAPI(title="Products API with DuckDB & Pagination")

# ---------- DB dependency ----------

def get_db():
    """
    Simple per-request DuckDB connection.
    For heavier use, you might pool or reuse connections.
    """
    con = connect(DB_PATH)
    try:
        yield con
    finally:
        con.close()


# ---------- Routes ----------

@app.get("/products", response_model=PaginatedProducts)
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=100),
    in_stock: Optional[bool] = Query(None),
    db: DuckDBPyConnection = Depends(get_db),
):
    """
    GET /products?page=1&page_size=5&in_stock=true

    Returns a paginated list of products with optional filtering.
    """

    # Build WHERE clause dynamically for filtering
    filters = []
    params = []

    if in_stock is not None:
        filters.append("in_stock = ?")
        params.append(in_stock)

    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)

    # Total count
    total_query = f"SELECT COUNT(*) FROM products {where_clause}"
    total = db.execute(total_query, params).fetchone()[0]

    if total == 0:
        return PaginatedProducts(
            items=[],
            total=0,
            page=page,
            page_size=page_size,
            pages=0,
        )

    # Pagination math
    offset = (page - 1) * page_size
    pages = (total + page_size - 1) // page_size  # ceiling division

    # Fetch page of rows
    data_query = f"""
        SELECT id, name, price, in_stock
        FROM products
        {where_clause}
        ORDER BY id
        LIMIT ? OFFSET ?
    """
    page_params = params + [page_size, offset]
    rows = db.execute(data_query, page_params).fetchall()

    items = [
        Product(id=row[0], name=row[1], price=row[2], in_stock=row[3])
        for row in rows
    ]

    return PaginatedProducts(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@app.get("/products/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: DuckDBPyConnection = Depends(get_db),
):
    """
    GET /products/1

    Returns a single product by ID.
    """
    row = db.execute(
        "SELECT id, name, price, in_stock FROM products WHERE id = ?",
        [product_id],
    ).fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found",
        )

    return Product(id=row[0], name=row[1], price=row[2], in_stock=row[3])


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: DuckDBPyConnection = Depends(get_db),
):
    """
    POST /products
    {
      "name": "New Item",
      "price": 12.34,
      "in_stock": true
    }

    Creates a new product and returns it.
    """

    # Get next id (simple example, not safe in concurrent multi-writer setups)
    next_id = db.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM products").fetchone()[0]

    db.execute(
        "INSERT INTO products (id, name, price, in_stock) VALUES (?, ?, ?, ?)",
        [next_id, product.name, product.price, product.in_stock],
    )

    return Product(id=next_id, **product.model_dump())


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: DuckDBPyConnection = Depends(get_db),
):
    """
    DELETE /products/1

    Deletes a product.
    """
    deleted = db.execute(
        "DELETE FROM products WHERE id = ? RETURNING id",
        [product_id],
    ).fetchone()

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found",
        )

    # No body for 204
    return