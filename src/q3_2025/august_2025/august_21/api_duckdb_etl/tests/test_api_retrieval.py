import pytest
from util.retrieve_api_response import get_posts, API_Exception

# Create a test
def test_api_response():
    assert isinstance(get_posts(), list)

# Mock Tests via requests-mock
def test_get_posts_success_with_mock(requests_mock):
    url = "https://jsonplaceholder.typicode.com/posts"

    # Generate sample data
    sample_data = [{'id': 7}]

    requests_mock.get(url, json=sample_data, status_code=200)

    assert get_posts() == sample_data

# Mock Failure Test
def test_get_posts_failure(requests_mock):
    url = "https://jsonplaceholder.typicode.com/posts"

    requests_mock.get(url, status_code=404)

    with pytest.raises(API_Exception):
        get_posts()