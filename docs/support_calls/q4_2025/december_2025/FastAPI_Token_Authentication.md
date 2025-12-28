# FastAPI + DuckDB Demo API (with API Keys)

- This tutorial walks you through building a small REST API that:

    - Serves JSON from a **DuckDB** table
    - Protects routes with an **API key** (a token)
    - Lets a user **register + log in** to receive an API key
    - Stores users + API keys in DuckDB (good for a demo)
    - Uses simple patterns you can reuse in bigger apps

---

## What you’ll build

### Public routes
- `POST /auth/register` → create a user account
- `POST /auth/login` → get an API key (token)

### Protected routes (require an API key)
- `GET /items` → list items from DuckDB
- `GET /items/{item_id}` → fetch one item from DuckDB
- `POST /auth/revoke` → revoke the token you’re currently using

---

## Key idea: API key in a request header

Clients must send a header like:

X-API-Key: sk_…some-long-token…

FastAPI can extract a header API key using `APIKeyHeader`, and you can enforce it with a dependency.

---

### Step 0 — Install packages

Create and activate a virtual environment if you want (recommended), then:

```bash
pip install fastapi uvicorn duckdb "passlib[bcrypt]"
```

- `duckdb` gives you an embedded SQL database in your Python process.
- `passlib[bcrypt]` helps safely hash and verify passwords using bcrypt.


### Step 1 — Create `main.py`

- Create a file named `main.py` and paste the following code:

```python
import duckdb
import secrets
import hashlib
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from datetime import datetime, timedelta, timezone

app = FastAPI(title="DuckDB + FastAPI + API Key Demo")

DB_PATH = "demo.duckdb"

# Extracts X-API-Key from incoming requests
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# ---------------------------
# Database helpers
# ---------------------------

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

@app.on_event("startup")
def startup():
    init_db()


# ---------------------------
# Request/response models
# ---------------------------

class RegisterIn(BaseModel):
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    api_key: str
    expires_at: datetime | None

class ItemOut(BaseModel):
    id: int
    name: str
    price: float


# ---------------------------
# Token + hashing helpers
# ---------------------------

def utcnow() -> datetime:
    return datetime.now(timezone.utc)

def make_api_key() -> str:
    # secrets is the standard library tool for generating secure tokens
    return "sk_" + secrets.token_urlsafe(32)

def hash_token(raw_token: str) -> str:
    # Deterministic hash so we can look it up quickly in DB
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


# ---------------------------
# Auth dependency (protect routes)
# ---------------------------

def require_api_key(raw_key: str = Depends(api_key_header)) -> dict:
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )

    token_h = hash_token(raw_key)
    conn = get_conn()

    row = conn.execute(
        """
        SELECT ak.user_id, ak.expires_at, ak.revoked
        FROM api_keys ak
        WHERE ak.token_hash = ?
        """,
        [token_h],  # parameterized query
    ).fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid API key")

    user_id, expires_at, revoked = row

    if revoked:
        conn.close()
        raise HTTPException(status_code=401, detail="API key revoked")

    if expires_at is not None and expires_at.replace(tzinfo=timezone.utc) < utcnow():
        conn.close()
        raise HTTPException(status_code=401, detail="API key expired")

    conn.execute(
        "UPDATE api_keys SET last_used_at = ? WHERE token_hash = ?",
        [utcnow(), token_h],
    )
    conn.close()

    return {"user_id": user_id}


# ---------------------------
# Auth routes (get a token)
# ---------------------------

@app.post("/auth/register", status_code=201)
def register(payload: RegisterIn):
    conn = get_conn()

    existing = conn.execute(
        "SELECT 1 FROM users WHERE email = ?",
        [payload.email],
    ).fetchone()

    if existing:
        conn.close()
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = int(conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM users;").fetchone()[0])
    pw_hash = bcrypt.hash(payload.password)

    conn.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?)",
        [user_id, payload.email, pw_hash, utcnow()],
    )

    conn.close()
    return {"message": "User registered. Now POST /auth/login to get an API key."}


@app.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn):
    conn = get_conn()

    row = conn.execute(
        "SELECT id, password_hash FROM users WHERE email = ?",
        [payload.email],
    ).fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_id, pw_hash = row
    if not bcrypt.verify(payload.password, pw_hash):
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    raw_token = make_api_key()
    token_h = hash_token(raw_token)

    key_id = int(conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM api_keys;").fetchone()[0])

    # Demo expiry: 30 days
    expires = utcnow() + timedelta(days=30)

    conn.execute(
        "INSERT INTO api_keys VALUES (?, ?, ?, ?, ?, FALSE, NULL)",
        [key_id, int(user_id), token_h, utcnow(), expires],
    )

    conn.close()
    return TokenOut(api_key=raw_token, expires_at=expires)


@app.post("/auth/revoke")
def revoke_my_key(me=Depends(require_api_key), raw_key: str = Depends(api_key_header)):
    conn = get_conn()
    conn.execute(
        "UPDATE api_keys SET revoked = TRUE WHERE token_hash = ?",
        [hash_token(raw_key)],
    )
    conn.close()
    return {"message": "API key revoked"}


# ---------------------------
# Data routes (protected)
# ---------------------------

@app.get("/items", response_model=list[ItemOut])
def list_items(me=Depends(require_api_key)):
    conn = get_conn()
    rows = conn.execute("SELECT id, name, price FROM items ORDER BY id;").fetchall()
    conn.close()
    return [ItemOut(id=r[0], name=r[1], price=r[2]) for r in rows]


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int, me=Depends(require_api_key)):
    conn = get_conn()
    row = conn.execute(
        "SELECT id, name, price FROM items WHERE id = ?",
        [item_id],
    ).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemOut(id=row[0], name=row[1], price=row[2])
```

Step 2 — Run the server

```bash
uvicorn main:app --reload
```

Open interactive docs:

- http://127.0.0.1:8000/docs

    - FastAPI automatically generates OpenAPI docs, and security dependencies integrate into that schema.

### Step 3 — Use the API end-to-end

1. Register a user

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"letmein123"}'
```

2. Login to get a token

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"letmein123"}'
```

You’ll receive:

```json
{"api_key":"sk_...","expires_at":"..."}
```

- This token was generated using Python’s secrets module, which is designed for generating secure tokens.

3. Call a protected route

```bash
curl http://127.0.0.1:8000/items \
  -H "X-API-Key: sk_...paste_yours_here..."
```

4. Revoke the current token

```bash
curl -X POST http://127.0.0.1:8000/auth/revoke \
  -H "X-API-Key: sk_...paste_yours_here..."
```

- After revoking, the same token should stop working.

---

### Why we hash secrets (passwords AND API keys)

#### Passwords

- We store password_hash (not the raw password). We used `bcrypt` via Passlib to hash() and verify() passwords.

#### API keys

- We return the raw API key to the user once, but we store only a hash (sha256) in the database.
That way, if the DB leaks, attackers don’t instantly get usable API keys.

#### Why parameterized queries matter

- Notice our SQL uses `?` placeholders and a separate list of values:

```python
conn.execute("SELECT ... WHERE email = ?", [payload.email])
```

- That’s a parameterized query pattern and is widely recommended to reduce SQL injection risk. DuckDB supports prepared/parameterized queries.


### What’s happening under the hood (mental model)
1.	`/auth/register` inserts a new row in users
2.	`/auth/login` verifies the password, then:
    - generates an API key
    - hashes it
    - stores the hash in api_keys
    - returns the raw key to the user
3.	Protected routes call require_api_key() first:
    - reads X-API-Key
    - hashes it
    - looks it up in DuckDB
    - blocks the request if missing/invalid/revoked/expired


### Common beginner mistakes (and fixes)

1. “Missing X-API-Key header”

    - You tried calling /items without including the header. 

    - Add:

```bash
-H "X-API-Key: sk_..."
```

2. “Invalid API key”

- Double-check you copied the token from /auth/login correctly.
- Also note: if you called /auth/revoke, that token won’t work anymore.


### Scaling notes (what you’d change in production)

- DuckDB is great for learning and local demos (it runs inside your app process).

- But for a real multi-user API, you’d typically:
	- Use PostgreSQL (or similar) for auth data (handles many concurrent writers)
	- Add indexes:
	- users(email)
	- api_keys(token_hash)
	- Add rate limiting (often Redis-backed), e.g. “100 requests/minute per API key”
	- Support multiple API keys per user (one per app/device) + “rotate keys”
	- Add roles/permissions if some users should access different data
	- If you need delegated auth (login through other apps) or more complex flows, consider OAuth2/JWT patterns supported by FastAPI’s security utilities.
