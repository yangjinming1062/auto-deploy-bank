# Stage 1: Build frontend assets
FROM node:20-alpine as builder
WORKDIR /app
COPY package.json .
RUN yarn install --prod --modules-folder ./openvpn_monitor/static/dist

# Stage 2: Final application image
FROM python:3.10-slim

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . .

# Copy built frontend assets from builder stage
COPY --from=builder /app/openvpn_monitor/static/dist /app/openvpn_monitor/static/dist

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV OPENVPNMONITOR_CONFIG_FILE=/app/openvpn-monitor.conf

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "openvpn_monitor.app:application"]