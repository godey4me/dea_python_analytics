from typing import List
from pydantic import BaseModel

# ---------- Pydantic models ----------

class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool


class ProductCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True


class PaginatedProducts(BaseModel):
    items: List[Product]
    total: int
    page: int
    page_size: int
    pages: int