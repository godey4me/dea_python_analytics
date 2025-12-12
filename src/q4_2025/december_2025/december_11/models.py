from pydantic import BaseModel
from typing import List

class Comment(BaseModel):

    # Attributes
    postId : int
    id: int
    name: str
    email: str
    body: str

class PaginatedItems(BaseModel):
    comments: List[Comment]
    total: int
    page: int
    page_size: int