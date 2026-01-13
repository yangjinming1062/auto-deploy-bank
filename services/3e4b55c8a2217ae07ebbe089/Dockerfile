# Multi-stage build for Amundsen Frontend
ARG METADATASERVICE_BASE
ARG SEARCHSERVICE_BASE

# Stage 1: Build React/Node.js frontend
FROM node:12-slim as node-stage
WORKDIR /app/amundsen_application/static

COPY ./frontend/amundsen_application/static/package.json /app/amundsen_application/static/package.json
COPY ./frontend/amundsen_application/static/package-lock.json /app/amundsen_application/static/package-lock.json
RUN npm install

COPY ./frontend/amundsen_application/static/ /app/amundsen_application/static/
RUN npm rebuild node-sass
RUN npm run dev-build

# Stage 2: Python application
FROM python:3.7-slim
WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./frontend/requirements.txt /app/requirements.txt
COPY ./frontend/requirements-dev.txt /app/requirements-dev.txt
COPY ./requirements-common.txt /app/requirements-common.txt

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-common.txt && \
    pip install --no-cache-dir "Jinja2<3.0" "markupsafe<2.0" "itsdangerous<2.0" && \
    pip install --no-cache-dir gunicorn==20.1.0

# Copy application code
COPY --from=node-stage /app /app
COPY ./frontend /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=amundsen_application
ENV METADATASERVICE_BASE=${METADATASERVICE_BASE}
ENV SEARCHSERVICE_BASE=${SEARCHSERVICE_BASE}

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

# Expose port
EXPOSE 5000

# Use gunicorn to run the application
CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:5000", "amundsen_application.wsgi:application"]