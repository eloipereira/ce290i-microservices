# Frontend - Streamlit App

A simple Streamlit application that visualizes user age distribution from the API.

## Features

- **Fetch Users**: Button to get all users from the API
- **Age Histogram**: Visual representation of user ages
- **Statistics**: Shows total users, average age, youngest, and oldest

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure the API is running on `http://localhost:8000`

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Docker Usage

```bash
# Build the image
docker build -t frontend-streamlit .

# Run the container
docker run -p 8501:8501 frontend-streamlit
```

## How it Works

1. Click "Get User Ages and Plot Histogram" button
2. App calls `/users/` endpoint
3. Extracts ages from all users
4. Creates a histogram using matplotlib
5. Displays statistics below the chart
