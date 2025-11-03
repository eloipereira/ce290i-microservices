# Data Ingestion Simulator

A Python script that generates fake user data and sends it to the User Management API to simulate continuous data ingestion.

## Features

- **Fake Data Generation**: Uses Faker library to create realistic user names
- **Random User Creation**: Generates random user IDs (1-10000) and ages (18-80)
- **Configurable Interval**: Adjustable delay between API calls
- **Health Check**: Waits for API availability before starting
- **Error Handling**: Graceful handling of connection errors and duplicate users

## Configuration

Environment variables:
- `API_BASE_URL`: Base URL of the User API (default: `http://localhost:8000`)
- `SIMULATION_INTERVAL`: Interval between requests in seconds (default: `5`)

## Running the Service

### Local Development
```bash
# Create and activate a virtual environment
python -m venv .venv

source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the simulator
python main.py
```
### With Docker
```bash
# Build the image
docker build -t data-simulator .

# Run the container (make sure API is running first)
docker run --name sim0 -e API_BASE_URL=http://localhost:8000 data-simulator
```

## Sample Output

```
2025-11-02 14:30:15 - INFO - API is ready!
2025-11-02 14:30:15 - INFO - Starting data ingestion simulation...
2025-11-02 14:30:15 - INFO - Created user: ID=1234, Name=Alice Johnson, Age=28
2025-11-02 14:30:20 - INFO - Created user: ID=5678, Name=Bob Smith, Age=34
2025-11-02 14:30:25 - ERROR - Failed to create user 1234: User already exists
```

## Dependencies

- `requests`: HTTP client for API calls
- `faker`: Generate fake user data
