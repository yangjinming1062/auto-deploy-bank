FROM python:3.3-slim

# The Debian Jessie repositories are archived. Update sources.list to point to the archive.
RUN sed -i 's/deb.debian.org/archive.debian.org/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/archive.debian.org\/debian-security/g' /etc/apt/sources.list && \
    sed -i '/jessie-updates/d' /etc/apt/sources.list

# Install build tools and curl, allowing unauthenticated packages from the expired archive.
RUN apt-get update && apt-get install -y --allow-unauthenticated build-essential curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY . .

# Install the package and its dependencies
RUN pip install --no-cache-dir .

CMD ["python", "examples/test/test.py"]
