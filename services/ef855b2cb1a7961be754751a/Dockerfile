FROM python:3.11

# Install system dependencies, including curl and ffmpeg
RUN apt-get update && apt-get install -y curl ffmpeg && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Configure poetry to create the virtual env in the project's root
RUN poetry config virtualenvs.in-project true

# Copy dependency definition files
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
# --no-dev excludes development dependencies like pytest
# This creates a .venv folder in /app
RUN poetry install --no-root --without dev

# Copy the application source code into the container
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# The CMD uses poetry run to execute commands within the virtual environment
CMD ["poetry", "run", "gunicorn", "--log-level", "debug", "--bind", "0.0.0.0:8000", "app:app"]
