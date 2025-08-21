from requests import get

# Custom Exception
class API_Exception(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def get_posts(base_url: str = 'https://jsonplaceholder.typicode.com/posts') -> list[dict]:

    # Result
    result = []

    # JSON response
    response = get(url=base_url)

    # Check status code
    if response.status_code == 200:
        result = response.json()
    
    else:
        raise API_Exception("Something went wrong with retrieving the posts. Check your URL or HTTP method.")
    
    return result