########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2025, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
#########################################################################

#########################################################################
# Create a Node container which will be used to build the JS components
# and clean up the web/ source code
#########################################################################

FROM alpine:latest AS app-builder

RUN apk add --no-cache \
    autoconf \
    automake \
    bash \
    g++ \
    git \
    libc6-compat \
    libjpeg-turbo-dev \
    libpng-dev \
    libtool \
    make \
    nasm \
    nodejs \
    npm \
    python3 \
    python3-dev \
    py3-setuptools \
    zlib-dev && \
    ln -sf /usr/bin/python3 /usr/bin/python

# Create the /pgadmin4 directory and copy the source into it. Explicitly
# remove the node_modules directory as we'll recreate a clean version, as well
# as various other files we don't want
COPY Makefile /pgadmin4/
COPY web /pgadmin4/web
RUN rm -rf /pgadmin4/web/*.log \
           /pgadmin4/web/config_*.py \
           /pgadmin4/web/node_modules \
           /pgadmin4/web/regression \
           `find /pgadmin4/web -type d -name tests` \
           `find /pgadmin4/web -type f -name .DS_Store`

WORKDIR /pgadmin4

# Build the JS vendor code in the app-builder, and then remove the vendor source.
RUN npm install -g corepack && corepack enable && make install-node

# Bundle the code and then remove the source. We'll copy the real code
# in later so it's current.
RUN make bundle
#########################################################################
# Next, create the base environment for Python
#########################################################################

FROM alpine:latest AS env-builder

# Install dependencies
COPY requirements.txt /
RUN apk add --no-cache \
        make \
        python3 \
        py3-pip && \
    apk add --no-cache --virtual build-deps \
        build-base \
        openssl-dev \
        libffi-dev \
        postgresql-dev \
        krb5-dev \
        rust \
        cargo \
        zlib-dev \
        libjpeg-turbo-dev \
        libpng-dev \
        python3-dev && \
    python3 -m venv --system-site-packages --without-pip /venv && \
    /venv/bin/python3 -m pip install --no-cache-dir -r requirements.txt && \
    apk del --no-cache build-deps

#########################################################################
# Assemble everything into the final container.
#########################################################################

FROM alpine:latest

# Copy in the Python packages
COPY --from=env-builder /venv /venv

WORKDIR /pgadmin4
ENV PYTHONPATH=/pgadmin4

# Copy in the code and docs
COPY --from=app-builder /pgadmin4/web/ /pgadmin4
COPY pkg/docker/run_pgadmin.py /pgadmin4
COPY pkg/docker/gunicorn_config.py /pgadmin4
COPY pkg/docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# License files
COPY LICENSE /pgadmin4/LICENSE
COPY DEPENDENCIES /pgadmin4/DEPENDENCIES

# Install runtime dependencies and configure everything in one RUN step
RUN apk add --no-cache \
        python3 \
        bash \
        py3-pip \
        postfix \
        krb5-libs \
        libjpeg-turbo \
        shadow \
        sudo \
        tzdata \
        libedit \
        libldap \
        libcap \
        curl postgresql-libs zstd-libs lz4-libs && \
    /venv/bin/python3 -m pip install --no-cache-dir gunicorn==23.0.0 && \
    find / -type d -name '__pycache__' -exec rm -rf {} + && \
    useradd -r -u 5050 -g root -s /sbin/nologin pgadmin && \
    mkdir -p /run/pgadmin /var/lib/pgadmin && \
    chown pgadmin:root /run/pgadmin /var/lib/pgadmin && \
    chmod g=u /var/lib/pgadmin && \
    touch /pgadmin4/config_distro.py && \
    chown pgadmin:root /pgadmin4/config_distro.py && \
    chown -R pgadmin:root /pgadmin4/static && \
    chmod g=u /pgadmin4/config_distro.py && \
    chmod g=u /etc/passwd && \
    setcap CAP_NET_BIND_SERVICE=+eip /usr/bin/python3.12 && \
    echo "pgadmin ALL = NOPASSWD: /usr/sbin/postfix start" > /etc/sudoers.d/postfix && \
    echo "pgadminr ALL = NOPASSWD: /usr/sbin/postfix start" >> /etc/sudoers.d/postfix

RUN chown pgadmin:root /pgadmin4

USER pgadmin

# Finish up
VOLUME /var/lib/pgadmin
EXPOSE 80 443

ENTRYPOINT ["/entrypoint.sh"]
