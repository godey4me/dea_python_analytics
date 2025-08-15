import pytest

@pytest.mark.parametrize("a,b,result", [
    (2, 3, 5),
    (-1, 1, 0),
    (10, 5, 15)
])
def test_add(a, b, result):
    assert a + b == result