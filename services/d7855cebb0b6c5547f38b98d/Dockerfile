FROM python:2.7-alpine

# Set working directory
WORKDIR /home/ubuntu/deploy-projects/d7855cebb0b6c5547f38b98d

# Install curl, PostgreSQL development libraries, and build tools
RUN apk add --no-cache curl postgresql-dev gcc python2-dev musl-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_SETTINGS=config.ProductionConfig
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Create database and start server
CMD /bin/sh -c "python db_create.py && gunicorn run:app --bind 0.0.0.0:8000 --workers 4"