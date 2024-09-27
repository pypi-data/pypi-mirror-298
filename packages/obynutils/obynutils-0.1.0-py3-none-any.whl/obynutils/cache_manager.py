import redis

class RedisCache:
    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def set(self, key, value, ttl=None):
        """Set a value in the Redis cache with an optional TTL (time-to-live)."""
        self.client.set(key, value, ex=ttl)

    def get(self, key):
        """Get a value from the Redis cache."""
        return self.client.get(key)

    def delete(self, key):
        """Delete a value from the Redis cache."""
        self.client.delete(key)
