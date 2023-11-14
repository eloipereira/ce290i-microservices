import csv
import logging
from typing import Any
from typing import Generator

from pydantic import ValidationError

from gps_replay.models import GPS


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
