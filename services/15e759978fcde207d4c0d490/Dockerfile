FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    mariadb-client \
    nodejs \
    npm \
    build-essential \
    libmariadb3 \
    libpq-dev \
    libmagic1 \
    fonts-liberation \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    libatspi2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Upgrade yarn to latest version
RUN npm install -g yarn@latest

# Set work directory
WORKDIR /app

# Copy Python dependencies
COPY pyproject.toml ./

# Install Python dependencies using pip
RUN python -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))" > /tmp/requirements.txt 2>/dev/null || \
    python -c "import tomli; print('\n'.join(toml_load(open('pyproject.toml', 'rb'))['project']['dependencies']))" > /tmp/requirements.txt 2>/dev/null || \
    printf "Babel~=2.13.1\nClick~=8.1.7\nfilelock~=3.13.1\nfiletype~=1.2.0\nGitPython~=3.1.34\nJinja2~=3.1.2\nPillow~=10.3.0\nPyJWT~=2.8.0\nPyMySQL==1.1.1\npypdf~=3.17.0\nPyPika==0.48.9\nPyQRCode~=1.2.1\nPyYAML~=6.0.1\nRestrictedPython~=8.0\nWeasyPrint==59.0\npydyf==0.10.0\nWerkzeug~=3.0.1\nWhoosh~=2.7.4\nbeautifulsoup4~=4.12.2\nbleach-allowlist~=1.0.3\nbleach[css]~=6.0.0\ncairocffi==1.5.1\nchardet~=5.1.0\ncroniter~=2.0.1\ncryptography~=43.0.1\ncssutils~=2.9.0\nemail-reply-parser~=0.5.12\ngunicorn @ git+https://github.com/frappe/gunicorn@72c1e495d89259151e73947a057432d528b06bb0\nhtml5lib~=1.1\nipython~=8.15.0\nldap3~=2.9\nmarkdown2~=2.4.8\nMarkupSafe>=2.1.0,<3\nmaxminddb-geolite2==2018.703\nnum2words~=0.5.12\noauthlib~=3.2.2\nopenpyxl~=3.1.2\npasslib~=1.7.4\npdfkit~=1.0.0\nphonenumbers==8.13.13\npremailer~=3.10.0\npsutil~=5.9.5\npsycopg2-binary~=2.9.1\npyOpenSSL~=24.2.1\npydantic~=2.7.0\npyotp~=2.8.0\npython-dateutil~=2.8.2\npytz==2023.3\nrauth~=0.7.3\nredis~=4.5.5\nhiredis~=2.2.3\nrequests-oauthlib~=1.3.1\nrequests~=2.32.0\nrq==1.15.1\nrsa>=4.1\nsemantic-version~=2.10.0\nsentry-sdk~=1.37.1\nsqlparse~=0.5.0\nsql_metadata~=2.11.0\ntenacity~=8.2.2\nterminaltables~=3.1.10\ntraceback-with-variables~=2.0.4\ntyping_extensions>=4.6.1,<5\ntomli~=2.0.1\nxlrd~=2.0.1\nzxcvbn~=4.4.28\nmarkdownify~=0.11.6\nboto3~=1.34.143\ndropbox~=11.36.2\ngoogle-api-python-client~=2.2.0\ngoogle-auth-oauthlib~=0.4.4\ngoogle-auth~=1.29.0\nposthog~=3.0.1\nvobject~=0.9.7\n" > /tmp/requirements.txt && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application code
COPY . .

# Create sites directory and apps.txt for esbuild
RUN mkdir -p /app/sites/assets /app/localhost/logs && \
    echo "frappe" > /app/sites/apps.txt && \
    echo "[]" > /app/sites/assets/assets.json && \
    touch /app/localhost/logs/frappe.log /app/localhost/logs/database.log

# Create logs directory symlink
RUN ln -sf /app/localhost/logs /logs

# Create site_config.json with database configuration in the correct location
RUN printf '{"db_name": "frappe", "db_password": "frappe", "db_host": "mariadb", "db_port": 3306, "db_user": "frappe", "redis_cache": "redis://redis:6379", "redis_queue": "redis://redis:6379"}' > /app/sites/localhost/site_config.json

# Make startup script executable
RUN chmod +x /app/start.sh

# Install frontend dependencies and build assets
ENV FRAPPE_BENCH_ROOT=/app
RUN yarn install --production=true && yarn production

# Create non-root user
RUN useradd -m -u 1000 frappe && chown -R frappe:frappe /app
USER frappe

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/method/frappe.ping

# Expose port
EXPOSE 8000

# Start command
CMD ["/app/start.sh"]