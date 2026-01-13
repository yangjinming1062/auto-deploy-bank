FROM python:3.8-slim

# Install curl for healthcheck and postgresql client library for psycopg2
RUN apt-get update && apt-get install -y curl libpq-dev build-essential && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .
RUN rm -f config.env .env

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "manage:app"]
