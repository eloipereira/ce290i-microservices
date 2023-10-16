import logging

import redis

from data_layer.config import RedisConfig
from data_layer.gps import replay_from_csv_to_redis

cfg = RedisConfig()

try:
    db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port, decode_responses=True)
    replay_from_csv_to_redis("data/dataset_gps.csv", redis=db)
except redis.ConnectionError as e:
    logging.error(msg=f"Redis connection error: {e}")
