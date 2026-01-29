## Streamlit and FastAPI Caching Guide

### Table of Contents
- [Streamlit Caching Mechanisms](#streamlit-caching-mechanisms)
- [FastAPI Caching Strategies](#fastapi-caching-strategies)
- [Sharing Data Between Streamlit and FastAPI](#sharing-data-between-streamlit-and-fastapi)
- [Common Patterns and Gotchas](#common-patterns-and-gotchas)
- [When to Scale: Moving to Redis/Memcache](#when-to-scale-moving-to-redismemcache)

---

## Streamlit Caching Mechanisms

Streamlit provides two primary caching decorators as of version 1.18+:

### 1. `@st.cache_data` - For Data Operations

Use this for functions that return data (DataFrames, lists, dicts, etc.):

```python
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(file_path):
    """Cache data loading operations"""
    return pd.read_csv(file_path)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_api_data(endpoint):
    """Cache API calls with TTL"""
    response = requests.get(endpoint)
    return response.json()

@st.cache_data(max_entries=10)  # Keep only 10 most recent entries
def process_query(query_params):
    """Limit cache size for frequently changing inputs"""
    return perform_expensive_computation(query_params)
```

**Key Features:**
- Creates a new copy of the data on each access (mutation-safe)
- Automatically handles serialization
- Best for: DataFrames, lists, dicts, JSON data
- TTL (Time To Live) support
- Max entries limitation

### 2. `@st.cache_resource` - For Shared Resources

Use this for non-serializable objects like database connections, ML models:

```python
@st.cache_resource
def get_database_connection():
    """Singleton pattern for DB connection"""
    return psycopg2.connect(
        host="localhost",
        database="mydb",
        user="user",
        password="password"
    )

@st.cache_resource
def load_ml_model():
    """Cache heavy ML models"""
    return joblib.load('model.pkl')

@st.cache_resource
def get_session_state():
    """Share state across reruns"""
    return {"counter": 0, "data": []}
```

**Key Features:**
- Returns the SAME object on each access (not a copy)
- Best for: DB connections, ML models, API clients
- Shared across all users and sessions
- Not serialized

### 3. Legacy Caching (Pre-1.18)

```python
# OLD - Still works but deprecated
@st.cache(allow_output_mutation=True)
def old_cache_function():
    return some_data
```

---

## FastAPI Caching Strategies

### 1. In-Memory Caching with `functools.lru_cache`

```python
from fastapi import FastAPI
from functools import lru_cache
import time

app = FastAPI()

@lru_cache(maxsize=128)
def expensive_computation(param: str):
    """Simple in-memory caching"""
    time.sleep(2)  # Simulate expensive operation
    return f"Result for {param}"

@app.get("/compute/{param}")
async def compute_endpoint(param: str):
    return {"result": expensive_computation(param)}
```

**Limitations:**
- Single process only (doesn't work with multiple workers)
- No TTL support
- Limited size control

### 2. Custom Cache Manager

```python
from fastapi import FastAPI
from datetime import datetime, timedelta
from typing import Optional, Any
import asyncio

class CacheManager:
    def __init__(self):
        self._cache = {}
        self._timestamps = {}

    def get(self, key: str, ttl: int = 300) -> Optional[Any]:
        """Get cached value if not expired"""
        if key in self._cache:
            if datetime.now() - self._timestamps[key] < timedelta(seconds=ttl):
                return self._cache[key]
            else:
                # Expired
                del self._cache[key]
                del self._timestamps[key]
        return None

    def set(self, key: str, value: Any):
        """Set cache value"""
        self._cache[key] = value
        self._timestamps[key] = datetime.now()

    def clear(self):
        """Clear all cache"""
        self._cache.clear()
        self._timestamps.clear()

# Global cache instance
cache = CacheManager()

app = FastAPI()

@app.get("/data/{item_id}")
async def get_data(item_id: str):
    # Check cache
    cached = cache.get(f"item_{item_id}", ttl=600)
    if cached:
        return {"data": cached, "from_cache": True}

    # Compute and cache
    result = await fetch_from_database(item_id)
    cache.set(f"item_{item_id}", result)
    return {"data": result, "from_cache": False}
```

### 3. Using Middleware for Response Caching

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import hashlib
import json

app = FastAPI()
response_cache = {}

@app.middleware("http")
async def cache_middleware(request: Request, call_next):
    # Only cache GET requests
    if request.method != "GET":
        return await call_next(request)

    # Create cache key from URL
    cache_key = hashlib.md5(str(request.url).encode()).hexdigest()

    if cache_key in response_cache:
        return JSONResponse(content=response_cache[cache_key])

    response = await call_next(request)

    # Cache the response (simplified)
    if response.status_code == 200:
        response_cache[cache_key] = {"status": "from_cache"}

    return response
```

---

## Sharing Data Between Streamlit and FastAPI

### Pattern 1: Shared Database

The most common approach - both apps connect to the same database:

```python
# shared_db.py
import psycopg2
from functools import lru_cache

@lru_cache()
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="shared_db",
        user="user",
        password="password"
    )

# streamlit_app.py
import streamlit as st
from shared_db import get_db_connection

@st.cache_resource
def get_connection():
    return get_db_connection()

@st.cache_data(ttl=60)
def load_data_from_db():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM data", conn)

# FastAPI app
from fastapi import FastAPI
from shared_db import get_db_connection

app = FastAPI()

@app.get("/data")
async def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    return cursor.fetchall()
```

### Pattern 2: FastAPI as Data Source for Streamlit

Streamlit calls FastAPI endpoints:

```python
# fastapi_app.py
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

app = FastAPI()

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())

@app.get("/api/data")
@cache(expire=60)
async def get_cached_data():
    # Expensive operation
    return {"data": compute_expensive_data()}

# streamlit_app.py
import streamlit as st
import requests

@st.cache_data(ttl=60)
def fetch_from_api():
    response = requests.get("http://localhost:8000/api/data")
    return response.json()

st.write(fetch_from_api())
```

### Pattern 3: Shared File System Cache

Both apps read/write from shared cache files:

```python
# shared_cache.py
import pickle
import os
from datetime import datetime, timedelta
from pathlib import Path

CACHE_DIR = Path("/tmp/shared_cache")
CACHE_DIR.mkdir(exist_ok=True)

class FileCache:
    @staticmethod
    def get(key: str, ttl: int = 300):
        cache_file = CACHE_DIR / f"{key}.pkl"
        if cache_file.exists():
            if datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime) < timedelta(seconds=ttl):
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
        return None

    @staticmethod
    def set(key: str, value):
        cache_file = CACHE_DIR / f"{key}.pkl"
        with open(cache_file, 'wb') as f:
            pickle.dump(value, f)

# Usage in both apps
data = FileCache.get("my_data")
if data is None:
    data = expensive_computation()
    FileCache.set("my_data", data)
```

### Pattern 4: Shared In-Memory Store (Single Server)

Using global Python objects (works only on single server):

```python
# shared_state.py
from datetime import datetime

class SharedCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cache = {}
            cls._instance.timestamps = {}
        return cls._instance

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value
        self.timestamps[key] = datetime.now()

# Both apps can import and use
shared_cache = SharedCache()
```

**Warning:** This only works if Streamlit and FastAPI run in the same Python process.

---

## Common Patterns and Gotchas

### Gotcha 1: Cache Key Collisions

```python
# BAD - Same cache key for different users
@st.cache_data
def get_user_data(user_id):
    return fetch_data(user_id)

# GOOD - Include all relevant parameters
@st.cache_data
def get_user_data(user_id, date_range, filters):
    return fetch_data(user_id, date_range, filters)
```

### Gotcha 2: Mutable Objects in `@st.cache_resource`

```python
# DANGEROUS - Shared mutable object
@st.cache_resource
def get_shared_list():
    return []

# User A appends item - ALL users see it!
shared = get_shared_list()
shared.append("item")  # This affects everyone!

# SAFE - Return new copy each time
@st.cache_data
def get_user_list():
    return []
```

### Gotcha 3: Unhashable Parameters

```python
# BAD - Lists and dicts aren't hashable
@st.cache_data
def process(items: list):  # Error!
    return sum(items)

# GOOD - Convert to hashable types
@st.cache_data
def process(items: tuple):
    return sum(items)

# Or use hash_funcs (legacy)
@st.cache_data(hash_funcs={list: lambda x: tuple(x)})
def process(items: list):
    return sum(items)
```

### Gotcha 4: Database Connection in `@st.cache_data`

```python
# BAD - Connection objects can't be serialized
@st.cache_data
def get_connection():
    return psycopg2.connect(...)  # Error!

# GOOD - Use cache_resource for connections
@st.cache_resource
def get_connection():
    return psycopg2.connect(...)
```

### Gotcha 5: Forgetting TTL for Time-Sensitive Data

```python
# BAD - Data never refreshes
@st.cache_data
def get_stock_prices():
    return fetch_latest_prices()

# GOOD - Add appropriate TTL
@st.cache_data(ttl=60)  # Refresh every minute
def get_stock_prices():
    return fetch_latest_prices()
```

### Gotcha 6: Multi-Worker FastAPI Cache Inconsistency

```python
# BAD - With uvicorn --workers 4, each worker has separate cache
cache = {}

@app.get("/data")
def get_data():
    if "data" not in cache:
        cache["data"] = expensive_op()
    return cache["data"]

# GOOD - Use Redis or external cache for multi-worker
```

### Pattern 1: Cache Warming

```python
# Warm cache on startup
@app.on_event("startup")
async def warm_cache():
    # Pre-populate frequently accessed data
    cache.set("common_data", load_common_data())
```

### Pattern 2: Cache Invalidation

```python
@st.cache_data
def get_data(version: int):
    """Version param allows manual cache busting"""
    return load_data()

# In Streamlit
if st.button("Refresh Data"):
    st.session_state.version = st.session_state.get("version", 0) + 1

data = get_data(st.session_state.get("version", 0))
```

### Pattern 3: Conditional Caching

```python
def smart_cache(func):
    """Only cache if data is expensive to compute"""
    def wrapper(*args, **kwargs):
        size = kwargs.get("size", 0)
        if size > 1000:  # Only cache large datasets
            return st.cache_data(func)(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper
```

---

## When to Scale: Moving to Redis/Memcache

### Signs You Need External Caching

1. **Multiple Servers/Workers**
   - Running FastAPI with multiple workers (uvicorn --workers 4)
   - Load-balanced Streamlit instances
   - In-memory cache creates inconsistency across workers

2. **Memory Constraints**
   - Cache size exceeds available RAM
   - Application crashes due to memory issues
   - Need to cache large datasets (>1GB)

3. **Cache Persistence Requirements**
   - Need cache to survive application restarts
   - Want to pre-populate cache before deployment
   - Sharing data across different applications

4. **Complex Invalidation Needs**
   - Need to invalidate cache from external triggers
   - Require pattern-based invalidation (delete all keys matching "user_*")
   - Time-based expiration with millisecond precision

5. **Performance at Scale**
   - Serving thousands of requests per second
   - Need sub-millisecond cache access
   - Handling concurrent cache updates

### Implementing Redis Caching

#### Installation

```bash
pip install redis fastapi-cache2[redis] streamlit
```

#### FastAPI with Redis

```python
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/expensive")
@cache(expire=300)  # 5 minutes
async def expensive_endpoint(param: str):
    result = perform_heavy_computation(param)
    return {"result": result}

@app.post("/invalidate/{key}")
async def invalidate_cache(key: str):
    """Manually invalidate cache entries"""
    await FastAPICache.clear(namespace=key)
    return {"status": "cleared"}
```

#### Streamlit with Redis

```python
import streamlit as st
import redis
import pickle
import hashlib

@st.cache_resource
def get_redis_client():
    return redis.Redis(host='localhost', port=6379, db=0)

def redis_cache(ttl=300):
    """Custom Redis cache decorator for Streamlit"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_data = f"{func.__name__}:{args}:{kwargs}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()

            redis_client = get_redis_client()

            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return pickle.loads(cached)

            # Compute and cache
            result = func(*args, **kwargs)
            redis_client.setex(cache_key, ttl, pickle.dumps(result))
            return result
        return wrapper
    return decorator

@redis_cache(ttl=600)
def load_large_dataset(query):
    # This will be cached in Redis
    return expensive_database_query(query)

# Usage
data = load_large_dataset("SELECT * FROM large_table")
```

#### Shared Redis Cache Between Apps

```python
# shared_redis_cache.py
import redis
import pickle
from typing import Any, Optional

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache"""
        data = self.client.get(key)
        if data:
            return pickle.loads(data)
        return None

    def set(self, key: str, value: Any, ttl: int = 300):
        """Set value in Redis cache with TTL"""
        self.client.setex(key, ttl, pickle.dumps(value))

    def delete(self, key: str):
        """Delete specific key"""
        self.client.delete(key)

    def delete_pattern(self, pattern: str):
        """Delete all keys matching pattern"""
        for key in self.client.scan_iter(match=pattern):
            self.client.delete(key)

    def clear(self):
        """Clear all cache"""
        self.client.flushdb()

# Both apps use the same cache
cache = RedisCache()

# FastAPI usage
@app.get("/data/{item_id}")
async def get_item(item_id: str):
    data = cache.get(f"item:{item_id}")
    if not data:
        data = fetch_from_db(item_id)
        cache.set(f"item:{item_id}", data, ttl=600)
    return data

# Streamlit usage
def get_user_data(user_id):
    data = cache.get(f"user:{user_id}")
    if not data:
        data = load_user_data(user_id)
        cache.set(f"user:{user_id}", data, ttl=300)
    return data
```

### Memcached Alternative

```python
from pymemcache.client import base

class MemcachedClient:
    def __init__(self, host='localhost', port=11211):
        self.client = base.Client((host, port))

    def get(self, key: str):
        return self.client.get(key)

    def set(self, key: str, value: bytes, expire: int = 300):
        self.client.set(key, value, expire=expire)

    def delete(self, key: str):
        self.client.delete(key)

# Usage similar to Redis
```

### Migration Strategy: From In-Memory to Redis

```python
# Step 1: Abstract cache interface
class CacheInterface:
    def get(self, key: str): pass
    def set(self, key: str, value: Any, ttl: int = 300): pass
    def delete(self, key: str): pass

# Step 2: Implement both backends
class InMemoryCache(CacheInterface):
    def __init__(self):
        self._cache = {}
    # ... implementation

class RedisCache(CacheInterface):
    def __init__(self, redis_url):
        self.client = redis.from_url(redis_url)
    # ... implementation

# Step 3: Use environment variable to switch
import os

def get_cache() -> CacheInterface:
    if os.getenv("USE_REDIS", "false") == "true":
        return RedisCache(os.getenv("REDIS_URL"))
    return InMemoryCache()

# Step 4: Use consistently
cache = get_cache()
```

### Performance Comparison

| Solution | Latency | Throughput | Persistence | Multi-Server | Memory Limit |
|----------|---------|------------|-------------|--------------|--------------|
| In-Memory | <1ms | Very High | No | No | RAM |
| Redis | 1-5ms | High | Yes | Yes | Configurable |
| Memcached | 1-3ms | Very High | No | Yes | Configurable |
| File System | 10-100ms | Low | Yes | Shared FS only | Disk |

### Best Practices for Production

1. **Use Redis for**:
   - Multi-server deployments
   - Cache persistence needs
   - Complex data structures
   - Pub/sub patterns

2. **Use Memcached for**:
   - Simple key-value caching
   - Maximum throughput
   - When persistence isn't needed

3. **Keep In-Memory for**:
   - Single-server deployments
   - Development environments
   - Very high-frequency access (>10k req/s)
   - Small cache sizes (<100MB)

4. **Monitoring & Alerts**:
```python
# Track cache hit rate
cache_hits = 0
cache_misses = 0

def get_with_metrics(key):
    global cache_hits, cache_misses
    result = cache.get(key)
    if result:
        cache_hits += 1
    else:
        cache_misses += 1
    return result

# Expose metrics endpoint
@app.get("/metrics")
def metrics():
    hit_rate = cache_hits / (cache_hits + cache_misses) if (cache_hits + cache_misses) > 0 else 0
    return {"hit_rate": hit_rate, "hits": cache_hits, "misses": cache_misses}
```

---

## Summary

- **Streamlit**: Use `@st.cache_data` for data, `@st.cache_resource` for connections/models
- **FastAPI**: Start with `lru_cache`, move to custom managers, then Redis for scale
- **Sharing Data**: Database, API calls, or shared cache layer (Redis)
- **Scale to Redis when**: Multiple workers, memory constraints, or need persistence
- **Common Gotchas**: Unhashable params, mutable objects, forgotten TTLs, multi-worker inconsistency

