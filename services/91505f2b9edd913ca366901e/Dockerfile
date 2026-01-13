FROM python:3.11-slim

# Install system dependencies including curl for healthcheck and Node.js for frontend build
RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NODE_ENV=production

# Set work directory
WORKDIR /app

# Copy source code first for setuptools-scm
COPY cms/ ./cms/
COPY menus/ ./menus/
COPY setup.py ./
COPY pyproject.toml ./
COPY MANIFEST.in ./

# Install Python dependencies from pyproject.toml
# Install dependencies without installing the package itself to avoid setuptools-scm issues
RUN pip install --no-cache-dir \
    "Django>=4.2" \
    "django-classy-tags>=0.7.2" \
    "django-formtools>=2.1" \
    "django-treebeard>=4.3" \
    "django-sekizai>=0.7" \
    "djangocms-admin-style>=1.5" \
    "dj-database-url" \
    "djangocms-text" \
    setuptools setuptools-scm

# Copy package.json and install Node dependencies (including devDependencies)
COPY package*.json ./
RUN npm install --include=dev

# Copy gulpfile and webpack config for building
COPY gulpfile.js ./
COPY webpack.config.js ./

# Build frontend assets using gulp bundle
RUN ./node_modules/.bin/gulp bundle

# Copy the rest of the application
COPY . .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Expose port
EXPOSE 8000

# Initialize database and start server
CMD sh -c "echo 'Initializing database...' && python manage.py migrate --run-syncdb 2>&1 || echo 'Migration failed, continuing...' && echo 'Starting server...' && python manage.py runserver 0.0.0.0:8000"