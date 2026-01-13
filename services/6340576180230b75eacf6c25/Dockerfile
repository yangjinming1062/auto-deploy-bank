# Google Cloud Platform Java Samples - Root Dockerfile
# This is a multi-module repository with 70+ independent samples.
# Each module has its own Dockerfile in its subdirectory.

# For the image-processing sample, use: run/image-processing/Dockerfile
# This root-level Dockerfile provides an overview of available modules.

FROM busybox:latest

LABEL maintainer="Google Cloud Samples"
LABEL description="Google Cloud Platform Java Samples - Multi-Module Repository"
LABEL url="https://github.com/GoogleCloudPlatform/java-docs-samples"

# Echo available modules
RUN echo "This repository contains 70+ independent Google Cloud service samples." && \
    echo "Individual module Dockerfiles:" && \
    echo "  - run/image-processing/" && \
    echo "  - run/helloworld/" && \
    echo "  - run/system-package/" && \
    echo "  - run/pubsub/" && \
    echo "  - eventarc/pubsub/" && \
    echo "  - eventarc/audit-storage/" && \
    echo "" && \
    echo "To build a specific sample:" && \
    echo "  cd run/image-processing && docker compose up -d"

CMD ["echo", "Use module-specific Dockerfiles"]