from fastapi import FastAPI

# Object for the FastAPI class
app = FastAPI()

# Routes
@app.get(path='/test')
def test():
    return {
        'message': 'This is a test.'
    }

