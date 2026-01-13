FROM python:3.11-slim

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install gunicorn
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install the local Flask-Admin package with all extras
# This will also install flask-babel, flask-sqlalchemy etc.
RUN pip install --no-cache-dir .[all]

# Make entrypoint script executable (it was copied by 'COPY . .')
RUN chmod +x /app/entrypoint.sh

# Change working directory to the example app
WORKDIR /app/examples/sqla

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "admin:app"]
