FROM python:3.7-slim

# Install system packages
RUN apt-get update && apt-get install -y curl build-essential libenchant-2-2 zlib1g-dev libjpeg-dev libpng-dev libfreetype6-dev liblcms2-dev libffi-dev && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV BUILDBOT_VERSION=1.8.0

WORKDIR /app

# Copy files
COPY master/ ./master/
COPY worker/ ./worker/
COPY pkg/ ./pkg/
COPY master.cfg .
COPY buildbot.tac .
COPY create_user.py .
COPY setup_compat.sh .
COPY migrate_shim.py .
COPY start.sh .

# Make start script executable
RUN chmod +x start.sh

# Install dependencies - upgrade setuptools first for better pkg_resources support
RUN pip install --no-cache-dir --upgrade 'setuptools>=45.0'
RUN pip install --no-cache-dir 'zope-interface>=5.0' 'SQLAlchemy>=1.1.0,<1.2.0' 'sqlalchemy-migrate==0.12.0' 'Jinja2>=2.1' 'Twisted>=17.9.0' 'python-dateutil>=1.5' 'txaio>=2.2.2' 'autobahn>=0.16.0' 'PyJWT>=1.5' 'PyYAML>=3.10' 'future>=0.16' 'MarkupSafe>=0.23' 'six>=1.10.0' 'requests>=2.0' 'buildbot-www==1.8.0'

# Install buildbot
RUN pip install -e ./master && \
    pip install -e ./worker && \
    pip install -e ./pkg

# Setup compatibility
RUN python3 setup_compat.sh

EXPOSE 8080 9989

CMD ["./start.sh"]