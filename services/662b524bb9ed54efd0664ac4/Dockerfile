FROM python:3.12-slim

# Install curl, netcat, openssh-client, and sudo for healthcheck, MySQL wait, SSH key generation, and sudo commands
RUN apt-get update && apt-get install -y curl netcat-openbsd openssh-client sudo && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV HTTP_HOST=
ENV CREATE_TEST_ACCOUNTS=false

# Set work directory
WORKDIR /home/ubuntu/deploy-projects/662b524bb9ed54efd0664ac4

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt setuptools

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /var/log/roxy-wi \
    /var/lib/roxy-wi/keys \
    /var/lib/roxy-wi/configs/hap_config \
    /var/lib/roxy-wi/configs/kp_config \
    /var/lib/roxy-wi/configs/nginx_config \
    /var/lib/roxy-wi/configs/apache_config \
    /etc/roxy-wi \
    /home/ubuntu/deploy-projects/662b524bb9ed54efd0664ac4/scripts

# Copy and set up config file
COPY roxy-wi.cfg /etc/roxy-wi/roxy-wi.cfg

# Generate SSH keys for JWT authentication if they don't exist
RUN if [ ! -f /var/lib/roxy-wi/keys/roxy-wi-key ]; then \
    ssh-keygen -t rsa -b 2048 -f /var/lib/roxy-wi/keys/roxy-wi-key -N "" -q; \
    fi

# Ensure proper permissions
RUN chmod 600 /var/lib/roxy-wi/keys/roxy-wi-key \
    && chmod 644 /var/lib/roxy-wi/keys/roxy-wi-key.pub \
    && chmod 644 /etc/roxy-wi/roxy-wi.cfg \
    && chmod +x /home/ubuntu/deploy-projects/662b524bb9ed54efd0664ac4/scripts/entrypoint.sh

# Expose the application port
EXPOSE 8765

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8765/ || exit 1

# Run the Flask application via entrypoint
ENTRYPOINT ["/home/ubuntu/deploy-projects/662b524bb9ed54efd0664ac4/scripts/entrypoint.sh"]
CMD []