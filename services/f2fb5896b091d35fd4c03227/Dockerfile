FROM python:3.10-slim

# Install curl for healthcheck and other system dependencies
RUN apt-get update && apt-get install -y curl libgl1 libglib2.0-0 gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

COPY . .

# Install the project and its dependencies
RUN pip install --no-cache-dir .

# Expose the internal port
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "imaginairy.http_app.app:app", "--host", "0.0.0.0", "--port", "8080"]
