FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED=1

ENV HTTP_BIND_HOST=0.0.0.0

# Install system dependencies, including curl for healthcheck and git for VCS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    libldap2-dev \
    libsasl2-dev \
    libx11-dev \
    cron \
    ca-certificates \
    default-libmysqlclient-dev \
    openssh-client \
    sshpass \
    bubblewrap \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv, the package manager used by the project
RUN pip install uv

WORKDIR /opt/jumpserver

COPY . .

# Overwrite config.yml with production settings for docker-compose
RUN printf 'SECRET_KEY: random_string\n\
BOOTSTRAP_TOKEN: random_string\n\
DB_ENGINE: postgresql\n\
DB_HOST: postgres\n\
DB_PORT: 5432\n\
DB_USER: jumpserver\n\
DB_PASSWORD: password\n\
DB_NAME: jumpserver\n\
REDIS_HOST: redis\n\
REDIS_PORT: 6379\n' > config.yml

# Compile dependencies from pyproject.toml to requirements.txt
RUN uv pip compile pyproject.toml -o requirements.txt

# Install python dependencies from the generated requirements.txt
RUN uv pip install --system -r requirements.txt

# Ensure the entrypoint script is executable
RUN chmod +x ./entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["./entrypoint.sh"]
CMD ["start", "all"]
