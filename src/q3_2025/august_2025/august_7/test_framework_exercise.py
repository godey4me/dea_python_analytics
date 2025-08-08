pass_count = 0
total_tests = 0

# Decorator

## Outer function
def test_tracker(func):
    # Inner function
    def wrapper(*args, **kwargs) -> tuple:

        # # Variables in the global scope need to be mentioned with the global keyword inside of an inner function
        global pass_count, total_tests

        # Update your total_tests by 1
        total_tests += 1

        print(total_tests)
        print(pass_count)

        # Exception Handling
        try:
            # Execute the test
            func(*args, **kwargs) # AssertionError
            pass_count += 1
            print(f"{func.__name__} passed!")
        
        except AssertionError:
            print(f"{func.__name__} failed.")
        
        return pass_count, total_tests
        
    return wrapper




