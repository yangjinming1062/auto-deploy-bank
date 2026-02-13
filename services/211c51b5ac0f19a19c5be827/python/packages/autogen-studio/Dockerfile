FROM python:3.10-slim

WORKDIR /code

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install autogenstudio and mcp dependency
RUN pip install --no-cache-dir -U autogenstudio mcp

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    AUTOGENSTUDIO_HOST=0.0.0.0 \
    AUTOGENSTUDIO_PORT=8081 \
    AUTOGENSTUDIO_API_DOCS=False \
    AUTOGENSTUDIO_CLEANUP_INTERVAL=300 \
    AUTOGENSTUDIO_SESSION_TIMEOUT=3600 \
    AUTOGENSTUDIO_DEFAULT_USER_ID=guestuser@gmail.com \
    AUTOGENSTUDIO_UPGRADE_DATABASE=False \
    AUTOGENSTUDIO_LITE_MODE=False \
    AUTOGENSTUDIO_AUTH_DISABLED=True \
    AUTOGENSTUDIO_AUTH_TYPE=none

# Create a non-root user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    AUTOGENSTUDIO_APPDIR=/home/user/app

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

EXPOSE 8081

CMD ["python3", "run.py"]