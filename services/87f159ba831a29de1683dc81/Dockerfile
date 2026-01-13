# Stage 1: Build frontend assets
FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Stage 2: Final Python application image
FROM python:3.9-slim
# Install build-essential for uwsgi compilation, added comment to break cache again and again and again and again.
RUN apt-get update && apt-get install -y curl libpq-dev build-essential python3-dev libmagic1 && rm -rf /var/lib/apt/lists/*
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
COPY --from=builder /app/ckan/public ./ckan/public
# Re-install requirements to include python-magic
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .
EXPOSE 5000
CMD ["uwsgi", "--ini", "ckan-uwsgi.ini"]