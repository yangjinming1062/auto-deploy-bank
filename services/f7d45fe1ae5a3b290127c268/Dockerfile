# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install curl for healthchecks and libatomic1 for prisma
RUN apt-get update && apt-get install -y curl libatomic1 && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
# This leverages Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Generate prisma client
RUN prisma generate

# Expose the internal port the application runs on
EXPOSE 4000

# Command to run the application
CMD ["uvicorn", "litellm.proxy.proxy_server:app", "--host", "0.0.0.0", "--port", "4000"]
