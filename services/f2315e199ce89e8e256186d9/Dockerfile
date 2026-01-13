# Use a slim Python 2.7 base image
FROM python:2.7-slim

# Fix outdated Debian "Buster" repositories and install dependencies
RUN echo "deb http://archive.debian.org/debian/ buster main\ndeb http://archive.debian.org/debian-security/ buster/updates main" > /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends curl git && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies for MySQL, Redis, and Memcached
RUN pip install --no-cache-dir PyMySQL redis python-memcached

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Clone the correct version of web2py and initialize submodules
RUN git clone https://github.com/web2py/web2py.git && \
    cd web2py && \
    git checkout v2.19.1 && \
    git submodule update --init --recursive

# Copy the user's application code into the web2py applications folder
COPY applications/ /app/web2py/applications/

# Set the final working directory
WORKDIR /app/web2py

# Expose the port the app runs on
EXPOSE 8000

# The command to run the application
CMD ["python", "web2py.py", "--no_gui", "--no_banner", "-a", "a", "-i", "0.0.0.0", "-p", "8000"]
