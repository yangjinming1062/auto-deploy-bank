FROM python:3.9-slim

LABEL maintainer="Kitware, Inc. <kitware@kitware.com>"

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    SETUPTOOLS_SCM_PRETEND_VERSION_FOR_GIRDER=99.99.99

RUN apt-get update && apt-get install -y \
    gcc \
    libpython3-dev \
    git \
    libldap2-dev \
    libsasl2-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LJ https://github.com/krallin/tini/releases/download/v0.19.0/tini -o /sbin/tini && \
    chmod +x /sbin/tini

# Use nvm to install node
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash

# Default node version
RUN . ~/.bashrc && \
    nvm install 14 && \
    nvm alias default 14 && \
    nvm use default && \
    ln -s $(dirname `which npm`) /usr/local/node

ENV PATH="/usr/local/node:$PATH"

WORKDIR /home/ubuntu/deploy-projects/f4005490879ccd58108d45e1

COPY setup.py README.rst MANIFEST.in ./
COPY requirements.txt ./
COPY girder/ ./girder/
COPY plugins/ ./plugins/

RUN pip install --no-cache-dir --upgrade pip setuptools wheel setuptools-scm

RUN python setup.py bdist_wheel \
    && cd dist && pip install --no-cache-dir *.whl \
    && cd .. \
    && rm -rf build dist

COPY . .

RUN girder build && \
    rm -rf /root/.npm \
    /usr/local/lib/python3.9/site-packages/girder/web_client/node_modules

EXPOSE 8080

ENTRYPOINT ["/sbin/tini", "--", "girder", "serve"]

CMD ["--host", "0.0.0.0", "--port", "8080"]