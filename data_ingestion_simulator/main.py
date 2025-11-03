#!/usr/bin/env python3
"""
Simple data ingestion simulator that creates random fake users
by calling the /users/ POST API endpoint every 5 seconds.
"""

import logging
import os
import random
import time

import requests
from faker import Faker

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize faker
fake = Faker()

SIMULATION_INTERVAL: float = float(os.getenv("SIMULATION_INTERVAL", 5))  # seconds

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
CREATE_USER_ENDPOINT = f"{API_BASE_URL}/users/"
HEALTH_ENDPOINT = f"{API_BASE_URL}/docs"


def wait_for_api(max_retries: int = 30, delay: int = 2) -> bool:
    """Wait for the API to be available."""
    logger.info("Waiting for API to be available...")

    for attempt in range(max_retries):
        try:
            response = requests.get(HEALTH_ENDPOINT, timeout=5)
            if response.status_code == 200:
                logger.info("API is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        logger.info(f"API not ready, retrying in {delay}s... (attempt {attempt + 1}/{max_retries})")
        time.sleep(delay)

    logger.error("API failed to become available within timeout period")
    return False


def create_random_user() -> None:
    """Create a random user using faker and send to API."""
    user_id = random.randint(1, 10000)
    name = fake.name()
    age = random.randint(18, 80)  # Generate random age between 18 and 80

    payload = {"user_id": user_id, "name": name, "age": age}

    try:
        response = requests.post(CREATE_USER_ENDPOINT, params=payload)
        if response.status_code == 200:
            logger.info(f"Created user: ID={user_id}, Name={name}, Age={age}")
        else:
            logger.error(f"Failed to create user: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error: Make sure the FastAPI server is running on {API_BASE_URL}")
    except Exception as e:
        logger.error(f"Error: {e}")


def main() -> None:
    """Main loop to generate users every {SIMULATION_INTERVAL} seconds."""
    logger.info(f"Starting data ingestion simulator with interval {SIMULATION_INTERVAL} seconds...")

    # Wait for API to be available
    if not wait_for_api():
        logger.error("Exiting: API is not available")
        return

    logger.info(f"Sending random users to /users/ endpoint every {SIMULATION_INTERVAL} seconds")
    logger.info("Press Ctrl+C to stop")
    logger.info("-" * 50)

    try:
        while True:
            create_random_user()
            time.sleep(SIMULATION_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Stopping data ingestion simulator...")


if __name__ == "__main__":
    main()
