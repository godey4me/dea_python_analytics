from os import getcwd
from duckdb import connect

DB_PATH = getcwd() + "/data/duckdb/example.duckdb"

def init_db():
    con = connect(DB_PATH)

    con.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price DOUBLE,
            in_stock BOOLEAN
        )
    """)

    # Clear & seed
    con.execute("DELETE FROM products")

    data = [
        (1, "Laptop", 1299.99, True),
        (2, "Keyboard", 79.99, True),
        (3, "Mouse", 39.99, True),
        (4, "Monitor", 299.99, False),
        (5, "USB-C Hub", 59.99, True),
        (6, "Webcam", 89.99, True),
        (7, "Headphones", 149.99, False),
        (8, "Desk Lamp", 24.99, True),
        (9, "Microphone", 199.99, True),
        (10, "Chair", 249.99, True),
        (11, "Desk", 399.99, False),
    ]

    con.executemany(
        "INSERT INTO products (id, name, price, in_stock) VALUES (?, ?, ?, ?)",
        data
    )

    con.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized:", DB_PATH)