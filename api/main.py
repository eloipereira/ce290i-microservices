import logging

from fastapi import FastAPI
from fastapi import HTTPException

from . import crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy"}


@app.post("/users/")
def create_user(user_id: int, name: str, age: int):
    logger.info(f"Creating user: {user_id}, {name}, age: {age}")
    return crud.create_user(user_id, name, age)


@app.get("/users/{user_id}")
def get_user(user_id: int):
    logger.info(f"Getting user: {user_id}")
    user = crud.get_user(user_id)
    if "error" in user:
        logger.error(f"Error getting user: {user['error']}")
        raise HTTPException(status_code=404, detail=user["error"])
    return user


@app.get("/users/")
def get_all_users():
    logger.info("Getting all users")
    return crud.get_all_users()


@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, age: int):
    logger.info(f"Updating user: {user_id}, {name}, age: {age}")
    user = crud.get_user(user_id)
    if "error" in user:
        logger.error(f"Error updating user: {user['error']}")
        raise HTTPException(status_code=404, detail=user["error"])
    return crud.update_user(user_id, name, age)


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    logger.info(f"Deleting user: {user_id}")
    user = crud.get_user(user_id)
    if "error" in user:
        logger.error(f"Error deleting user: {user['error']}")
        raise HTTPException(status_code=404, detail=user["error"])
    return crud.delete_user(user_id)
