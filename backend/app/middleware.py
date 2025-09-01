import time
from flask import request, jsonify
from functools import wraps
from collections import defaultdict

buckets = defaultdict(lambda: {"tokens": 10.0, "last": time.time()})
RATE_LIMIT = 10.0   # tokens per window
WINDOW_SEC = 60.0   # window length in seconds

def token_bucket_limit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            from flask_login import current_user
            key = (getattr(current_user, "id", "anon"), request.endpoint)
        except Exception:
            key = ("anon", request.endpoint)
        b = buckets[key]
        now = time.time()
        elapsed = now - b["last"]
        refill = (elapsed / WINDOW_SEC) * RATE_LIMIT
        b["tokens"] = min(RATE_LIMIT, b["tokens"] + refill)
        b["last"] = now
        if b["tokens"] < 1.0:
            return jsonify({"error": "Too Many Requests"}), 429
        b["tokens"] -= 1.0
        return fn(*args, **kwargs)
    return wrapper
