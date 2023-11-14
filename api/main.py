import json
import time
from uuid import UUID
from uuid import uuid4

import redis
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import FastAPI

from gps_replay.config import RedisConfig
from gps_replay.models import GPS

cfg = RedisConfig()


def get_redis_db():
    db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port)
    try:
        yield db
    finally:
        db.close()


api = FastAPI(title="Vehicle Data API")


@api.get("/gps_state")
def get_gps_state_from_redis(redis_db=Depends(get_redis_db)) -> GPS:
    gps = redis_db.get("gps_state")
    return GPS(**json.loads(gps))


@api.get("/compute_avg_speed")
def compute_avg_speed(time_window_seconds: float, redis_db=Depends(get_redis_db)):
    speeds = []
    start = time.time()
    while time.time() - start <= time_window_seconds:
        state = json.loads(redis_db.get("gps_state"))
        speeds.append(state["speed_meters_per_second"])
    return sum(speeds) / len(speeds)


def compute_avg_speed_task(
    task_id: UUID, time_window_seconds: float, redis_db=Depends(get_redis_db)
):
    speeds = []
    start = time.time()
    while time.time() - start <= time_window_seconds:
        state = json.loads(redis_db.get("gps_state"))
        speeds.append(state["speed_meters_per_second"])
    redis_db.set(
        f"task:{task_id}",
        json.dumps({"status": "DONE", "result": sum(speeds) / len(speeds)}),
    )


@api.post("/request_to_compute_avg_speed")
def request_to_compute_avg_speed(
    time_window_seconds: float,
    background_tasks: BackgroundTasks,
    redis_db=Depends(get_redis_db),
):
    task_id = uuid4()
    redis_db.set(f"task:{task_id}", json.dumps({"status": "REQUESTED"}))
    background_tasks.add_task(
        compute_avg_speed_task, task_id, time_window_seconds, redis_db
    )
    return task_id


@api.get("/get_avg_speed_task_status")
def get_avg_speed_task_status(task_id: UUID, redis_db=Depends(get_redis_db)):
    return redis_db.get(f"task:{task_id}")
