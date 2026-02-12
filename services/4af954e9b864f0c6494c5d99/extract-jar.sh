#!/bin/bash
set -e

# Extract target.jar from the built image for security scanning
docker run --rm --entrypoint sh 4af954e9b864f0c6494c5d99-vikunja -c "cat /app/vikunja/target.jar" > target.jar

echo "target.jar extracted successfully"
ls -la target.jar