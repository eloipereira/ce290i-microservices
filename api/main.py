import redis
from fastapi import Depends
from fastapi import FastAPI

from data_layer.config import RedisConfig
from data_layer.models import GPS

cfg = RedisConfig()


def get_redis_db():
    db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port)
    try:
        yield db
    finally:
        db.close()


api = FastAPI(title="Vehicle Data API")


@api.get("/gps_state")
def get_gps_state_from_redis(redis_db=Depends(get_redis_db)):
    return redis_db.get("gps_state")
