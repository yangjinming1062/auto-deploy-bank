# Use a slim Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies: curl for healthchecks, nodejs, npm for building, and git for setuptools-scm
RUN apt-get update && apt-get install -y curl nodejs npm git && \
    rm -rf /var/lib/apt/lists/*

# Install configurable-http-proxy, a runtime dependency
RUN npm install -g configurable-http-proxy

# Set the working directory
WORKDIR /app

# Copy all application files
COPY . .

# Install JS dependencies and run builds, as defined in setup.py.
RUN npm install --progress=false --unsafe-perm
RUN npm run css

# Build the JSX admin app from its directory
WORKDIR /app/jsx
RUN npm install --progress=false --unsafe-perm
RUN npm run build
WORKDIR /app

# Install the Python package itself
RUN pip install .
RUN pip install notebook

# Expose the application port
EXPOSE 8000

RUN useradd -m admin

# Start JupyterHub as a module to avoid PATH issues
CMD ["python", "-m", "jupyterhub.app"]
