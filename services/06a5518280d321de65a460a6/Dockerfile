# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies including curl for healthchecks
RUN apt-get update && apt-get install -y curl build-essential libffi-dev && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Install the application to make the 'wssh' command available
RUN pip install .

# Create a non-root user for security
RUN addgroup --system webssh && adduser --system --ingroup webssh webssh
RUN chown -R webssh:webssh /app
USER webssh

# Expose the internal port
EXPOSE 8888

# Set the command to run the application
CMD ["wssh"]
