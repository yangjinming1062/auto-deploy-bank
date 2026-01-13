# Use python:3.x-slim base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VENV_IN_PROJECT=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

# Set working directory
WORKDIR /app

# Install system dependencies including curl for healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    nodejs \
    npm \
    openssl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock* ./

# Copy the rest of the application first
COPY . .

# Install dependencies using pip with both proxy and extra_proxy groups
RUN pip install -e .[proxy,extra_proxy] --no-cache-dir

# Build Admin UI if script exists
RUN if [ -f "docker/build_admin_ui.sh" ]; then chmod +x docker/build_admin_ui.sh && ./docker/build_admin_ui.sh; fi

# Generate Prisma client using Python CLI
RUN if [ -f "schema.prisma" ]; then python -m prisma generate || echo "Prisma generation failed, skipping..."; fi

# Generate prisma client if schema exists (disabled due to schema version incompatibility)
# RUN if [ -f "schema.prisma" ]; then npx prisma generate; fi

# Run prisma migrations if needed
# RUN if [ -f "docker/migrate.sh" ]; then chmod +x docker/migrate.sh && ./docker/migrate.sh; fi

# Make entrypoint script executable
RUN if [ -f "docker/entrypoint.sh" ]; then chmod +x docker/entrypoint.sh; fi
RUN if [ -f "docker/prod_entrypoint.sh" ]; then chmod +x docker/prod_entrypoint.sh; fi

# Copy supervisord config if exists
RUN if [ -f "docker/supervisord.conf" ]; then cp docker/supervisord.conf /etc/supervisord.conf; fi

# Expose port 4000
EXPOSE 4000

# Use production entrypoint if it exists, otherwise use default
ENTRYPOINT ["docker/prod_entrypoint.sh"]

# Default command runs litellm on port 4000
CMD ["--port", "4000"]