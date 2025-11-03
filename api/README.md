# User Management API

A simple FastAPI-based microservice for managing users with CRUD operations.

## Features

- **Create Users**: Add new users with ID, name, and age
- **Read Users**: Get individual users or list all users
- **Update Users**: Modify existing user information
- **Delete Users**: Remove users from the system
- **Health Check**: Monitor service health

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Get a specific user
- `GET /users/` - Get all users
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

## Data Structure

Users are stored as tuples in memory: `(name, age)`

Example response:
```json
{
  "1234": {"name": "John Smith", "age": 35},
  "5678": {"name": "Jane Doe", "age": 28}
}
```

## Running the Service


### Local Development
```bash
# Create and activate a virtual environment
python -m venv .venv

source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
fastapi dev main.py
```


### With Docker
```bash
# Build the image
docker build -t user-api .

# Run the container
docker run -p 8000:8000 user-api
```


## Testing

Access the interactive API documentation at: `http://localhost:8000/docs`

### Example cURL commands:
```bash
# Create a user
curl -X POST "http://localhost:8000/users/?user_id=123&name=Alice&age=30"

# Get a user
curl "http://localhost:8000/users/123"

# Get all users
curl "http://localhost:8000/users/"

# Update a user
curl -X PUT "http://localhost:8000/users/123?name=Alice%20Johnson&age=31"

# Delete a user
curl -X DELETE "http://localhost:8000/users/123"
```

## Docker Container Inspection

To understand how the Dockerfile commands created the container environment:

### Explore the API Container
```bash
# Enter the running API container
docker exec -it api /bin/bash

# Check the working directory (set by WORKDIR /app)
pwd  # Shows: /app

# See the files copied by COPY commands
ls -la
# main.py, crud.py, requirements.txt, __init__.py, __pycache__/

# Check installed Python packages (from pip install)
pip list
# Shows: fastapi, uvicorn, and dependencies

# Check the Python path
which python  # Shows: /usr/local/bin/python

# See the running processes
ps aux
# Shows: FastAPI/uvicorn process

# Check environment variables
env | grep -i fast

# Exit the container
exit
```

### Compare Container vs Host
```bash
# Container isolation demonstration
docker exec api ls /app/          # Container files
ls ./api/                         # Host files (same content, different filesystem)

# Container has its own process space
docker exec api ps aux            # Container processes
ps aux | grep fastapi             # Host processes (won't see FastAPI unless running locally)
```

This demonstrates how Docker creates an isolated environment with its own filesystem, processes, and network stack while sharing the host OS kernel.
