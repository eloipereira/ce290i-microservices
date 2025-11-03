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
    """
    Yields a Redis database instance connected to the host and port specified
    in the `RedisConfig` instance. The database connection is automatically
    closed when the generator is exited.

    Yields:
        redis.Redis: A Redis database instance
    """
    db = redis.Redis(host=cfg.redis_host, port=cfg.redis_port)
    try:
        yield db
    finally:
        db.close()


api = FastAPI(title="Vehicle Data API")


@api.get("/gps_state")
def get_gps_state_from_redis(redis_db=Depends(get_redis_db)) -> GPS:
    """
    Returns the current GPS state of the vehicle.

    Returns:
        GPS: The current GPS state of the vehicle
    """
    gps = redis_db.get("gps_state")
    return GPS(**json.loads(gps))


@api.get("/compute_avg_speed")
def compute_avg_speed(time_window_seconds: float, redis_db=Depends(get_redis_db)) -> float:
    """
    Computes the average speed over a specified time window.

    Args:
        time_window_seconds: The time window in seconds over which to compute
            the average speed.

    Returns:
        float: The average speed over the specified time window.
    """
    speeds = []
    start = time.time()
    while time.time() - start <= time_window_seconds:
        state = json.loads(redis_db.get("gps_state"))
        speeds.append(state["speed_meters_per_second"])
    return sum(speeds) / len(speeds)


def compute_avg_speed_task(
    task_id: UUID, time_window_seconds: float, redis_db=Depends(get_redis_db)
):
    """
    Computes the average speed over a specified time window.

    Args:
        task_id: A unique identifier for the task.
        time_window_seconds: The time window in seconds over which to compute
            the average speed.
        redis_db: The Redis database instance to use for computing the average
            speed.

    Returns:
        None
    """
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
    """
    Requests that the average speed be computed over a specified time window.

    Args:
        time_window_seconds: The time window in seconds over which to compute
            the average speed.
        background_tasks: A FastAPI dependency that provides a BackgroundTasks
            instance, which is used to schedule the computation of the average
            speed as a background task.
        redis_db: The Redis database instance to use for computing the average
            speed.

    Returns:
        The UUID of the task that was scheduled to compute the average speed.
    """
    task_id = uuid4()
    redis_db.set(f"task:{task_id}", json.dumps({"status": "REQUESTED"}))
    background_tasks.add_task(compute_avg_speed_task, task_id, time_window_seconds, redis_db)
    return task_id


@api.get("/get_avg_speed_task_status")
def get_avg_speed_task_status(task_id: UUID, redis_db=Depends(get_redis_db)):
    """
    Retrieves the status and result of a previously requested average speed
    computation task.

    Args:
        task_id: The unique identifier for the task whose status is to be
            retrieved.
        redis_db: The Redis database instance, provided by dependency injection.

    Returns:
        The status and result of the task as a JSON-encoded string.
    """
    return redis_db.get(f"task:{task_id}")
