# Stage 1: Build frontend assets
FROM node:12-buster-slim AS frontend-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i '/buster-updates/d' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y python2 make g++ --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Final application image
FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y curl postgresql-client build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /srv/misago
COPY requirements.txt requirements-plugins.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r requirements-plugins.txt
COPY . .
COPY --from=frontend-builder /app/misago/static/ /srv/misago/misago/static/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
