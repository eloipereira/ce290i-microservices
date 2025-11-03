# CE290i Microservices Project

A simple microservices architecture demonstration with three services: a User Management API, a Data Ingestion Simulator, and a Frontend Dashboard.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Data Ingestion │───▶│   User API       │◀───│   Frontend      │
│  Simulator      │    │   (FastAPI)      │    │   (Streamlit)   │
│  (Faker + HTTP) │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        │                        │                        │
        ▼                        ▼                        ▼
   Creates fake             Stores users              Visualizes
   users every             in memory as               age distribution
   few seconds             (name, age) tuples        as histogram
```

## Services

### 1. **User Management API** (`/api`)
- **Technology**: FastAPI
- **Port**: 8000
- **Purpose**: RESTful API for user CRUD operations
- **Features**: Create, read, update, delete users with health checks

### 2. **Data Ingestion Simulator** (`/data_ingestion_simulator`)
- **Technology**: Python + Faker
- **Purpose**: Generates and sends fake user data to the API
- **Features**: Configurable intervals, realistic fake data, error handling

### 3. **Frontend Dashboard** (`/frontend`)
- **Technology**: Streamlit
- **Port**: 8501
- **Purpose**: Web interface to visualize user age distribution
- **Features**: Interactive histogram, real-time data fetching, statistics

## Local Development (No Docker)

### Prerequisites
- Python 3.8+
- pip

### Run API Service:
```bash
cd api
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
# API available at http://localhost:8000
```

### Run Data Ingestion Simulator:
```bash
cd data_ingestion_simulator
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Run Frontend:
```bash
cd frontend
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
# Frontend available at http://localhost:8501
```


## Manual Docker Setup (Individual Services)

### Step 1: Create Network
```bash
docker network create microservices
```

### Step 2: Build Images
```bash
docker build -t user-api ./api
docker build -t data-simulator ./data_ingestion_simulator
docker build -t frontend-app ./frontend
```

### Step 3: Run Services (in order)

#### Start API Service:
```bash
docker run \
  --name api0 \
  --network microservices \
  -p 8000:8000 \
  user-api
```

#### Start Data Ingestion Simulator:
```bash
docker run \
  --name sim0 \
  --network microservices \
  -e API_BASE_URL=http://api0:8000 \
  -e SIMULATION_INTERVAL=5 \
  data-simulator
```

#### Start Frontend:
```bash
docker run \
  --name frontend0 \
  --network microservices \
  -p 8501:8501 \
  -e API_URL=http://api:8000/users/ \
  frontend-app
```

### Step 4: Verify Services
```bash
# Check running containers
docker ps

# View logs
docker logs api0
docker logs sim0
docker logs frontend0
```

## Quick Start (Docker Compose)

The easiest way to run all services together:

```bash
# Clone the repository
git clone <repository-url>
cd ce290i-microservices

# Start all services
docker-compose up --build

# Access the services
# - API Documentation: http://localhost:8000/docs
# - Frontend Dashboard: http://localhost:8501
```


## API Endpoints

Access the interactive API documentation at: `http://localhost:8000/docs`

- `GET /health` - Health check
- `POST /users/` - Create user (params: user_id, name, age)
- `GET /users/{user_id}` - Get specific user
- `GET /users/` - Get all users
- `PUT /users/{user_id}` - Update user (params: name, age)
- `DELETE /users/{user_id}` - Delete user


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

## Configuration

### Environment Variables

| Service | Variable | Default | Description |
|---------|----------|---------|-------------|
| Data Simulator | `API_BASE_URL` | `http://localhost:8000` | API base URL |
| Data Simulator | `SIMULATION_INTERVAL` | `5` | Seconds between requests |
| Frontend | `API_URL` | `http://localhost:8000/users/` | Full API endpoint URL |

## Cleanup

### Docker Compose:
```bash
docker-compose down
```

### Manual Docker:
```bash
# Stop containers
docker stop api0 sim0 frontend0

# Remove containers
docker rm api0 sim0 frontend0

# Remove network
docker network rm microservices

# Remove images (optional)
docker rmi user-api data-simulator frontend-app
```

## Educational Goals

This project demonstrates:
- **Microservices Architecture**: Independent, loosely coupled services
- **API Design**: RESTful API with proper HTTP methods
- **Service Communication**: HTTP-based inter-service communication
- **Containerization**: Docker for consistent deployment
- **Service Discovery**: Docker networking for service-to-service communication
- **Data Visualization**: Real-time data processing and visualization
- **Development vs Production**: Different deployment strategies

## Docker Container Inspection (Understanding Isolation)

To understand how Docker provides isolation and see the effects of Dockerfile commands, you can inspect running containers:

### Basic Container Inspection

```bash
# List running containers
docker ps

# Get detailed container information
docker inspect api0

# Check container resource usage
docker stats api0
```

### Exploring Container Filesystem

```bash
# Execute interactive shell inside the API container
docker exec -it api0 /bin/bash

# Or use sh if bash is not available
docker exec -it api0 /bin/sh
```

### Inside the Container - File System Exploration

Once inside the container, you can explore the filesystem and see how Dockerfile commands affected the environment:

```bash
# Check current working directory (set by WORKDIR in Dockerfile)
pwd
# Should show: /app

# List files in the working directory
ls -la
# You'll see: main.py, crud.py, requirements.txt, __pycache__/

# Check Python packages installed by pip install
pip list

# Explore the container's filesystem
ls /
# See root filesystem: bin, etc, usr, var, app, etc.

# Check environment variables
env | grep -i python

# See which Python executable is being used
which python
which fastapi

# Check the container's network configuration
cat /etc/hosts
# You'll see container hostname and network mappings

# Check running processes inside the container
ps aux
```

### Comparing Container vs Host

```bash
# Exit the container
exit

# Compare with host system
ls -la ./api/
# Same files but in host filesystem

# Check host Python environment (likely different)
pip list  # Your host packages

# Check host network
ifconfig  # Different network interfaces
```

### Understanding Docker Layers

```bash
# View the image layers and history
docker history user-api

# See what each Dockerfile command created
docker image inspect user-api
```

### Container Logs and Debugging

```bash
# View container logs
docker logs api0

# Follow logs in real-time
docker logs -f api0

# Check container processes from host
docker top api0
```

### File System Isolation Example

```bash
# Create a file inside the container
docker exec api0 touch /app/test-file.txt

# Check if file exists on host
ls ./api/test-file.txt  # File doesn't exist on host!

# The container filesystem is isolated from the host
docker exec api0 ls /app/  # File exists in container
```

### Network Isolation Example

```bash
# Check container's internal IP
docker exec api0 hostname -I

# Check container's view of network
docker exec api0 cat /etc/hosts

# Container has its own network namespace
# but can communicate through Docker networks
```

### Key Learning Points

1. **Filesystem Isolation**: Files created/modified inside containers don't affect the host
2. **Process Isolation**: Container processes are separate from host processes
3. **Network Isolation**: Each container has its own network interface
4. **Environment Isolation**: Different Python environments, packages, and configurations
5. **Resource Isolation**: Containers have their own CPU, memory limits (if set)

This demonstrates how Docker provides **operating system-level virtualization** without the overhead of full virtual machines.

## Technology Stack

- **Backend**: FastAPI (Python)
- **Data Generation**: Faker (Python)
- **Frontend**: Streamlit (Python)
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Networking**: Docker Bridge Networks
- **Data Storage**: In-memory (educational purposes)
