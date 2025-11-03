# Example of a simple in-memory database and crud methods (create, read, update, delete)
# Database stores user_id -> (name, age) tuples

db = {}


def create_user(user_id: int, name: str, age: int):
    if user_id in db:
        return {"error": "User already exists"}
    db[user_id] = (name, age)
    return {"message": "User created successfully"}


def get_user(user_id: int):
    user_data = db.get(user_id)
    if not user_data:
        return {"error": "User not found"}
    name, age = user_data
    return {"name": name, "age": age}


def update_user(user_id: int, name: str, age: int):
    if user_id not in db:
        return {"error": "User not found"}
    db[user_id] = (name, age)
    return {"message": "User updated successfully"}


def delete_user(user_id: int):
    if user_id not in db:
        return {"error": "User not found"}
    del db[user_id]
    return {"message": "User deleted successfully"}


def get_all_users() -> dict:
    # Convert tuple format to dictionary format for API response
    result = {}
    for user_id, (name, age) in db.items():
        result[user_id] = {"name": name, "age": age}
    return result
