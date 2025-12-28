from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from passlib.hash import bcrypt
from datetime import timedelta, timezone
from uvicorn import run

# Custom imports
from models import RegisterIn, LoginIn, TokenOut, ItemOut
from utils.db_util import get_conn, init_db
from utils.token_hashing_util import utcnow, make_api_key, hash_token

# FastAPI App
app = FastAPI(title="DuckDB + FastAPI + API Key Demo")

# Extracts X-API-Key from incoming requests
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# ---------------------------
# Auth dependency (protect routes)
# ---------------------------

def require_api_key(raw_key: str = Depends(api_key_header)) -> dict:
    if not raw_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )

    token_h = raw_key
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

# Setup DuckDB for the rest of the app
init_db()


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
    pw_hash = payload.password

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
    if not payload.password == pw_hash:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    raw_token = make_api_key()
    token_h = hash_token(raw_token)

    key_id = int(conn.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM api_keys;").fetchone()[0])

    # Demo expiry: 30 days
    expires = utcnow() + timedelta(days=30)

    conn.execute(
        "INSERT INTO api_keys VALUES (?, ?, ?, ?, ?, FALSE, NULL)",
        [key_id, int(user_id), raw_token, utcnow(), expires],
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


# Run the web server
run(app=app, host='0.0.0.0', port=8070)