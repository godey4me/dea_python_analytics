from fastapi import FastAPI, Query
from uvicorn import run
from requests import get

# Custom imports
from models import Comment, PaginatedItems

app = FastAPI()

# Routes
@app.get(path='/data')
def get_data(
    message: str = 'This is successful'
):
    return {
        'message' : message
    }

@app.get(path='/enhanced_comments')
def enhanced_comments(
    page: int = Query(description="Exact page number", ge=1, default=1),
    page_size: int = Query(
        default=50,
        ge=1,
        le=500,
        description="The exact number of comments to produce as a result."
    )
):
    
    # Response
    response: list[dict] = get('https://jsonplaceholder.typicode.com/comments').json()

    offset = (page - 1) * page_size
    end_idx = offset + page_size

    result = response[page - 1:page_size]

    result = [Comment(**obj) for obj in result]

    return PaginatedItems(
        comments=result,
        total=len(response),
        page=page,
        page_size=page_size
    )

run(app=app, host='0.0.0.0', port=8300)