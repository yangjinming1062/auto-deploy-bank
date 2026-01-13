# Use Python 3.12 slim as base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    libmagic1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22 (required by package.json)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy package files for npm install
COPY package.json package-lock.json* ./

# Install npm dependencies
RUN npm ci

# Copy entire source code
COPY . .

# Install Python dependencies from pyproject.toml
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .[testing]

# Workaround for CopyPlugin glob issue in Docker - comment out problematic patterns
RUN sed -i '/new CopyPlugin({/,/}),/s/^/\/\/ /' client/webpack.config.js

# Create static directories and manually copy files
RUN mkdir -p wagtail/admin/static wagtail/embeds/static wagtail/documents/static wagtail/images/static wagtail/contrib/search_promotions/static && \
    cp -r wagtail/admin/static_src/* wagtail/admin/static/ 2>/dev/null || true && \
    cp -r wagtail/embeds/static_src/* wagtail/embeds/static/ 2>/dev/null || true && \
    cp -r wagtail/documents/static_src/* wagtail/documents/static/ 2>/dev/null || true && \
    cp -r wagtail/images/static_src/* wagtail/images/static/ 2>/dev/null || true && \
    cp -r wagtail/contrib/search_promotions/static_src/* wagtail/contrib/search_promotions/static/ 2>/dev/null || true && \
    cp -r wagtail/contrib/typed_table_block/static_src/* wagtail/contrib/typed_table_block/static/ 2>/dev/null || true

# Build frontend assets
RUN npx webpack --config ./client/webpack.config.js --mode production

# Collect static files from test app
WORKDIR /app/wagtail/test && python manage.py collectstatic --noinput --clear

# Set work directory to test app for CMD
WORKDIR /app/wagtail/test

# Expose port
EXPOSE 8000

# Create superuser script
RUN echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
if not User.objects.filter(username='admin').exists(): \
    User.objects.create_superuser('admin', 'admin@example.com', 'changeme')" > /app/create_superuser.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start the server
CMD python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000