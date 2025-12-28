import duckdb
from os import getcwd

# ---------------------------
# Database helpers
# ---------------------------
DB_PATH = getcwd() + "/data/duckdb/fastapi_examples/demo.duckdb"


def get_conn():
    return duckdb.connect(DB_PATH)

def init_db():
    conn = get_conn()

    # Users table (email + password hash)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL
        );
    """)

    # API keys table (store only hashed tokens)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id BIGINT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            token_hash TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL,
            expires_at TIMESTAMP,
            revoked BOOLEAN NOT NULL DEFAULT FALSE,
            last_used_at TIMESTAMP
        );
    """)

    # Demo data table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id BIGINT PRIMARY KEY,
            name TEXT NOT NULL,
            price DOUBLE NOT NULL
        );
    """)

    # Seed items if empty
    count = conn.execute("SELECT COUNT(*) FROM items;").fetchone()[0]
    if count == 0:
        conn.execute("""
            INSERT INTO items VALUES
            (1, 'protein coffee', 4.99),
            (2, 'cold brew', 3.49),
            (3, 'matcha latte', 5.25);
        """)

    conn.close()