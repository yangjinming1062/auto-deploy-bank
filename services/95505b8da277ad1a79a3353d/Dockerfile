# Use a slim Python base image
FROM python:3.9-slim

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy files required for installation first to leverage caching
COPY requirements.txt .
COPY setup.py .
COPY setup.cfg .
COPY MANIFEST.in .
COPY README.md .
COPY CHANGELOG.md .
COPY httpx ./httpx

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Build the static documentation site
RUN python -m mkdocs build

# Set environment variable for unbuffered python output
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Serve the built documentation from the 'site' directory
CMD ["python", "-m", "http.server", "8000", "--directory", "site"]
