# Use the official Python image.
FROM python:3.9-slim

# Install curl, nodejs, npm, and git
RUN apt-get update && apt-get install -y curl nodejs npm git && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the entire project
COPY . .

# Install python dependencies from requirements files first to break the circular dependency
RUN pip install -r requirements/install.txt -r requirements/ci.txt -r requirements/dev.txt -r requirements/testing.txt -r requirements/celery.txt -r requirements/diskcache.txt

# Install gunicorn as it is not in the requirements files
RUN pip install gunicorn

# Install the local package in editable mode to make its console_scripts (e.g., `renderer`) available for the build step.
RUN pip install -e .

# Install node dependencies, skipping the husky prepare script which is not needed and fails outside a git repo
RUN npm ci --no-prepare

# Build frontend assets, which require the python dev deps
RUN npm run build

# Create an assets directory and copy the built assets to it
RUN mkdir /app/assets
RUN cp -r dash/dash-renderer/build/* /app/assets/

# Copy the example app to the root of the workdir
COPY tests/assets/simple_app.py app.py

# Command to run the app with gunicorn.
# The pip installs above already installed gunicorn and the main package (in editable mode).
CMD ["python", "-m", "gunicorn", "app:server", "--bind", "0.0.0.0:8050"]
