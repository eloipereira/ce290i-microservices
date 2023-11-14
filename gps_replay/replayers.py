import time

import redis

from gps_replay.ingestors import gps_generator_from_csv


def replay_gps_from_csv(csv_path: str):
    gps_gen = gps_generator_from_csv(csv_path=csv_path)
    for g in gps_gen:
        time.sleep(g.elapsed_time_seconds)
        results = g.model_dump_json()
        print(results)


def replay_gps_from_csv_to_redis_cache(csv_path: str, redis: redis.Redis):
    gps_gen = gps_generator_from_csv(csv_path=csv_path)
    for g in gps_gen:
        time.sleep(g.elapsed_time_seconds)
        redis.set("gps_state", g.model_dump_json())


def replay_gps_from_csv_to_redis_publisher(csv_path: str, redis: redis.Redis):
    gps_gen = gps_generator_from_csv(csv_path=csv_path)
    for g in gps_gen:
        time.sleep(g.elapsed_time_seconds)
        redis.set("gps_state", g.model_dump_json())
        redis.publish("gps_state_topic", g.model_dump_json())
