FROM python:3.11-slim

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install dependencies
COPY . .
RUN pip install .

# Create a dummy database file for Datasette
RUN touch dummy.db

# Expose the internal port for Datasette
EXPOSE 8001

# Set the command to run Datasette
CMD ["datasette", "serve", "-h", "0.0.0.0", "-p", "8001", "dummy.db"]
