FROM python:3.11-slim

WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl lsof && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers as root
RUN playwright install --with-deps

# Create a non-root user that will run the application
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser -d /home/appuser -m appuser

# Copy the downloaded browser binaries from root's cache to the appuser's cache
# and set the correct ownership. This allows the non-root user to access the browsers.
RUN mkdir -p /home/appuser/.cache/ms-playwright && \
    cp -r /root/.cache/ms-playwright/* /home/appuser/.cache/ms-playwright/ && \
    chown -R appuser:appuser /home/appuser/.cache

COPY . .

RUN pip install -r deploy/docker/requirements.txt

# Install the application from source
RUN pip install .

# Give the non-root user ownership of the application code
RUN chown -R appuser:appuser /app

EXPOSE 11235

# The CMD will run as root, but supervisord is configured to launch the actual application process as 'appuser'
CMD ["supervisord", "-c", "deploy/docker/supervisord.conf"]
