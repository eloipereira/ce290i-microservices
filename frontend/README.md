# User Age Distribution Frontend

A simple Streamlit web application that fetches user data from the User Management API and displays age distribution in a histogram.

## Features

- **Interactive Web Interface**: Simple button-driven UI
- **Real-time Data Fetching**: Gets latest user data from API
- **Age Distribution Visualization**: Histogram showing user age ranges
- **Statistics Display**: Shows total users, average age, min/max ages
- **Error Handling**: Graceful handling of API connection issues

## Configuration

Environment variables:
- `API_URL`: Full URL to the users endpoint (default: `http://localhost:8000/users/`)

## Running the Service

### Local Development
```bash
# Create and activate a virtual environment
python -m venv .venv

source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

### With Docker
```bash
# Build the image
docker build -t frontend-app .

# Run the container
docker run --name frontend0 -p 8501:8501 -e API_URL=http://localhost:8000/users/ frontend-app
```



## Usage

1. Open your browser to `http://localhost:8501`
2. Click "Get User Ages and Plot Histogram"
3. View the age distribution chart and statistics
4. Refresh data by clicking the button again

## Dependencies

- `streamlit`: Web application framework
- `requests`: HTTP client for API calls
- `matplotlib`: Plotting library for histograms
