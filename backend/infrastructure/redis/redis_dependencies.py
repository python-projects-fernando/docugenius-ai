import redis.asyncio as redis
import os

async def get_redis_client() -> redis.Redis:
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    password = os.getenv("REDIS_PASSWORD", None)
    db = int(os.getenv("REDIS_DB", 0))

    client = redis.Redis(
        host=host,
        port=port,
        password=password,
        db=db,
        decode_responses=True,
        health_check_interval=30,
    )
    return client