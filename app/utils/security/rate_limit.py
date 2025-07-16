import datetime
from flask import request

login_attempts = {}

def rate_limit(max_attempts=10, window_seconds=60):
    def decorator(f):
        async def wrapper(*args, **kwargs):
            ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            now = datetime.now(datetime.timezone.utc)
            attempts = login_attempts.get(ip,[])
            attempts = [attempt for attempt in attempts if (now - attempt).total_seconds() < window_seconds]
            if len(attempts) >= max_attempts:
                return {"error": "Too many login attempts. Please try again later."}, 429
            attempts.append(now)
            login_attempts[ip] = attempts
            return await f(*args, **kwargs)
        return wrapper
    return decorator