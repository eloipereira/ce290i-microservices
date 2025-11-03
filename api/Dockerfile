# Use Python 3.13 slim image
FROM python:3.13-slim

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy API files
COPY . .

# Expose port
EXPOSE 8000

# Launch FastAPI with uvicorn
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
