import logging

import redis
from gps_replay.config import RedisConfig

cfg = RedisConfig()


def subscriber(topic: str, redis: redis.Redis):
    pubsub = redis.pubsub()
    pubsub.subscribe(topic)
    for msg in pubsub.listen():
        if msg is not None and isinstance(msg, dict):
            logging.info(msg=msg)
            print(msg)


try:
    db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port, decode_responses=True)
    while True:
        subscriber(topic="gps_state_topic", redis=db)
except redis.ConnectionError as e:
    logging.error(msg=f"Redis connection error: {e}")
