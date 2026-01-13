# Dockerfile should instantiate AWS Project with configurable plugins
FROM python:3.8-slim
MAINTAINER Netflix Security
WORKDIR /apps/consoleme

# NODE_OPTIONS meeded to increase memory size of Node for the `yarn build` step. The Monaco Editor
# appears to be the culprit requiring this.
ENV NODE_OPTIONS="--max-old-space-size=20000"
ENV PYTHONUNBUFFERED=1

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    musl-dev \
    libcurl4-nss-dev \
    python3-dev \
    curl \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt clean && \
    apt update && \
    apt install -y nodejs npm && \
    npm install -g yarn

# Install watchdog. Used to automatically restart ConsoleMe in Docker, for development.
RUN pip install --no-cache-dir watchdog argh xmlsec

# Copy requirements first for better caching
COPY requirements.txt requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-test.txt --prefer-binary --force-reinstall

# Copy the rest of the application
COPY . /apps/consoleme
RUN pip install -e .

# Install SPA frontend
RUN yarn --cwd ui && \
    yarn --cwd ui build:prod

CMD ["python", "consoleme/__main__.py"]
EXPOSE 8081
