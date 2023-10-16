import csv
import logging
import time
from typing import Any
from typing import Generator

import redis
from pydantic import ValidationError

from data_layer.models import GPS


def gps_generator_from_csv(csv_path: str) -> Generator[GPS, Any, Any]:
    try:
        with open(csv_path) as file:
            csv_file = csv.DictReader(file)
            for line in csv_file:
                try:
                    yield GPS(**line)
                except ValidationError as error:
                    logging.error(msg=f"Data Validation Error: {error}")
    except IOError as e:
        logging.error(msg=f"IO Error: {e}")


def replay_from_csv_to_redis(csv_path: str, redis: redis.Redis, loop_back: bool = True):
    gps_gen = gps_generator_from_csv(csv_path=csv_path)
    for g in gps_gen:
        time.sleep(g.elapsed_time_seconds)
        print(g)
        redis.set("gps_state", g.model_dump_json())
