FROM node:20-bullseye-slim

# Install a lightweight web server
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY app/ ./app/

# Install http-server globally
RUN npm install -g http-server@14.1.1

# Expose port
EXPOSE 40010

# Command to run HTTP server
CMD ["http-server", "app", "-p", "40010", "--host", "0.0.0.0", "--cors"]