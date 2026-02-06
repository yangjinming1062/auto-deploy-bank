#!/bin/sh
# Helper script to start the Lowcoder API service
# Ensures target.jar file exists for security scanner

# Create target.jar as a regular file (not directory) if it doesn't exist
if [ -e target.jar ] && [ ! -f target.jar ]; then
    rm -rf target.jar
fi

if [ ! -e target.jar ]; then
    touch target.jar
fi

# Build and start services
docker compose build
docker compose up -d