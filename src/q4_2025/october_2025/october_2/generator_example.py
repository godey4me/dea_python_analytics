from typing import Generator

def generate_list(n: int = 10) -> list:

    return list(range(n+1))

def generate_list_v2(n: int = 10) -> Generator:

    # Loop through the range
    for i in range(n+1):

        # Yield keyword
        yield i

# List One
list_one = generate_list(n=100)


# List Two
list_two = generate_list_v2(n=100)

print(list_one)
print(list_two)

# Actually get the list
list_two = list(list_two)

print(list_two)