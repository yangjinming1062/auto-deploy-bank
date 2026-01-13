# Stage 1: Build frontend assets
FROM node:20-alpine as builder
WORKDIR /app
COPY package.json Gruntfile.js* ./
RUN npm install
COPY . .
RUN npm install -g grunt-cli
RUN grunt build

# Stage 2: Final application image
FROM python:3.8-slim
WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

# Copy python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application with built assets from the builder stage
COPY --from=builder /app/ .

# Copy configuration files to the location expected by the application
RUN mkdir -p /etc/confidant
COPY config/gunicorn.conf /etc/confidant/gunicorn.conf
COPY config/development/idp.crt /etc/confidant/idp.crt
COPY config/development/logging.conf /etc/confidant/logging.conf

EXPOSE 80

# Use the provided start command
CMD ["gunicorn", "--config", "/etc/confidant/gunicorn.conf", "confidant.wsgi:app", "--workers=2", "-k", "gevent", "--access-logfile=-", "--error-logfile=-"]