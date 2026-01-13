FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY django-todo-list/source_code_final/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application
COPY django-todo-list/source_code_final/ .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run migrations and start server
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000