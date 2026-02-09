FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/312057c7a639a8e25cc79244

# Copy dependency definitions
COPY pyproject.toml .

# Install dependencies from dev group (includes hypercorn, quart, quart-trio, trio, anyio)
RUN pip install --no-cache-dir "hypercorn[urllib3-changes]" quart quart-trio trio anyio trustme cryptography

# Copy source code with pre-generated _version.py
COPY src/ ./src/

# Install urllib3 by copying directly to site-packages (bypasses VCS detection)
RUN cp -r /home/ubuntu/deploy-projects/312057c7a639a8e25cc79244/src/urllib3 /usr/local/lib/python3.12/site-packages/ && \
    python -c "import urllib3; print(f'urllib3 version: {urllib3.__version__}')"

# Copy application code
COPY dummyserver/ ./dummyserver/
COPY start_server.py .

EXPOSE 8000

CMD ["python", "start_server.py"]