import redis
import json
import os

# Initialize Redis client
redis_client = None

# Lazy initialization function
def _get_redis_client():
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=int(os.getenv('REDIS_DB', 0)),
                password=os.getenv('REDIS_PASSWORD', None),
                socket_connect_timeout=2
            )
            # Test connection
            redis_client.ping()
        except Exception as e:
            print(f"Redis connection failed: {e}")
            redis_client = False  # Mark as failed
    return redis_client if redis_client is not False else None

def get_cache(key):
    """
    Get value from cache
    """
    client = _get_redis_client()
    if not client:
        return None
    
    try:
        value = client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Error getting cache: {e}")
        return None

def set_cache(key, value, expire=3600):
    """
    Set value in cache
    """
    client = _get_redis_client()
    if not client:
        return False
    
    try:
        client.setex(key, expire, json.dumps(value))
        return True
    except Exception as e:
        print(f"Error setting cache: {e}")
        return False
