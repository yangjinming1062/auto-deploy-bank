# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

RUN chmod +x ./run

# Create a non-privileged user
RUN useradd -ms /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

ENV PYTHONUNBUFFERED=1
ENV EXPOSE_PORT=5000

EXPOSE 5000

CMD ["./run"]