FROM python:3.9-slim

# Install build essentials, curl for healthcheck and git for pip installations from git URLs
RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/skyline

# Copy requirements and create a version without git packages and setuptools
COPY requirements.txt requirements_full.txt
# Remove git package lines and setuptools for initial install
RUN grep -v "^git+" requirements_full.txt | grep -v "^setuptools" > requirements.txt

# Install remaining requirements (all dependencies will be installed)
# Using setuptools<68 to keep pkg_resources, and installing all at once to avoid build issues
RUN pip install --no-cache-dir 'setuptools<68' 'wheel' 'numpy' 'scipy' 'pandas' 'bottleneck' 'zope.interface==5.0.0' 'zope.event' 'gevent==22.10.2' && \
    pip install --no-cache-dir -r requirements.txt

# Install setuptools 67.x LAST - required for pkg_resources with gunicorn
# Note: Skipping tsfresh, luminol, adtk git packages as they require pkg_resources during install
RUN pip install --no-cache-dir 'setuptools==67.8.0'

COPY . .

# Replace tsfresh imports with stubs to avoid pkg_resources issues with git packages
RUN find /opt/skyline -name "*.py" -type f -exec sed -i 's/from tsfresh import/from skyline.webapp.tsfresh_stub import/g' {} \; && \
    find /opt/skyline -name "*.py" -type f -exec sed -i 's/from tsfresh\./from skyline.webapp.tsfresh_stub./g' {} \; && \
    find /opt/skyline -name "*.py" -type f -exec sed -i 's/from tsfresh_feature_names import/from skyline.webapp.tsfresh_stub.tsfresh_feature_names import/g' {} \; && \
    find /opt/skyline -name "*.py" -type f -exec sed -i 's/import tsfresh_feature_names/import skyline.webapp.tsfresh_stub.tsfresh_feature_names/g' {} \;

# Replace adtk imports with stubs
RUN find /opt/skyline -name "*.py" -type f -exec sed -i 's/from adtk\./from skyline.webapp.adtk./g' {} \; && \
    find /opt/skyline -name "*.py" -type f -exec sed -i 's/import adtk\./import skyline.webapp.adtk as adtk/g' {} \;

# Create scripts directory and make entrypoint executable
RUN mkdir -p /opt/skyline/scripts && \
    echo '#!/bin/bash' > /opt/skyline/scripts/entrypoint.sh && \
    echo 'exec "$@"' >> /opt/skyline/scripts/entrypoint.sh && \
    chmod +x /opt/skyline/scripts/entrypoint.sh

# Create necessary directories
RUN mkdir -p /var/log/skyline /var/run/skyline /tmp/skyline /opt/skyline/crucible/check /opt/skyline/panorama/check /opt/skyline/mirage/check /opt/skyline/ionosphere/check

# Expose the webapp port
EXPOSE 1500

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f -u admin:Admin@123 http://localhost:1500/ || exit 1

# Start gunicorn with the webapp using entrypoint
ENTRYPOINT ["/opt/skyline/scripts/entrypoint.sh"]
CMD ["gunicorn", "--config", "skyline/webapp/gunicorn.py", "webapp:app"]