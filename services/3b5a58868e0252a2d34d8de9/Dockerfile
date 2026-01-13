# Use the official Python image.
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install system dependencies needed for the application
RUN apt-get update && apt-get install -y curl mariadb-client git && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install dependencies to leverage Docker cache
COPY requirements.txt ./
COPY extras-requirements.txt ./
COPY dockerfiles/mlrun-api/requirements.txt ./mlrun-api-requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r extras-requirements.txt -r mlrun-api-requirements.txt

# Copy the rest of the application code
COPY . .

# Install the application itself with all necessary extras for the api
RUN pip install .[complete-api]

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "-m", "server.api.main"]
