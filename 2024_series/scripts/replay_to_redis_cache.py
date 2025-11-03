import logging

import redis
from gps_replay.config import RedisConfig
from gps_replay.replayers import replay_gps_from_csv_to_redis_cache

cfg = RedisConfig()

try:
    db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port, decode_responses=True)
    replay_gps_from_csv_to_redis_cache("data/dataset_gps.csv", redis=db)
except redis.ConnectionError as e:
    logging.error(msg=f"Redis connection error: {e}")
