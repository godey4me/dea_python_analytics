import hashlib
import secrets
from datetime import datetime, timezone


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