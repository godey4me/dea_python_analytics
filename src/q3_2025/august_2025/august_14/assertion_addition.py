# test_math.py
def add(a, b):
    return a + b

def test_addition():
    assert add(2, 3) == 5  # Pass
    assert add(-1, 1) == 0  # Pass