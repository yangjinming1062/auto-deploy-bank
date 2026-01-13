FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Set the locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install base packages, python, curl, and add GNS3 PPA
# Using --no-install-recommends to keep the image smaller
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common curl locales python3-pip python3-dev && \
    add-apt-repository -y ppa:gns3/ppa && \
    apt-get update

# Install GNS3 dependencies
RUN apt-get install -y --no-install-recommends \
    qemu-system-x86 \
    qemu-kvm \
    libvirt-daemon-system \
    x11vnc \
    vpcs \
    ubridge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen en_US.UTF-8

WORKDIR /app

# Copy the entrypoint script
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copy and install Python dependencies for production for better layer caching
COPY requirements.txt dev-requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -r dev-requirements.txt

# Copy the rest of the application
COPY . .

# Remove the conflicting configuration file as per linter fix
RUN rm -rf conf

# Install the application itself
RUN pip3 install .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port and set the entrypoint
EXPOSE 3080
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python3", "-m", "gns3server", "--host", "0.0.0.0", "--port", "3080"]
