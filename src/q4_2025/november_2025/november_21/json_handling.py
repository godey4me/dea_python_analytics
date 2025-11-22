import polars as pl

data = [
    {
      "id": 1,
      "name": "Cole Volk",
      "fitness": {"height": 180, "weight": 85},
    },
    {
      "id": 2,
      "name": "Faye Raker",
      "fitness": {"height": 155, "weight": 58},
    },
    {
      "name": "Mark Reg",
      "fitness": {"height": 170, "weight": 78},
    },
]

df = pl.json_normalize(data, max_level=1)
print(df)

# Explode Example

df = pl.DataFrame({
    "letters": ["a", "a", "b", "c"],
    "numbers": [[1], [2,3], [4,5], [6,7,8]],
})

print("Before: ")
print(df)

exploded = df.explode("numbers")

print("After: ")
print(exploded)