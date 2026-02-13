#!/bin/bash
set -e

# Trap SIGTERM to keep container running
cleanup() {
  echo "Received signal, keeping alive..."
  sleep infinity
}
trap cleanup SIGTERM SIGINT

# Change to worker directory
cd /app/simple-worker

# Start wrangler in background
npx wrangler dev --local --port 8787 --ip 0.0.0.0 &
WRANGLER_PID=$!

# Wait for wrangler to be ready
echo "Waiting for wrangler to be ready..."
for i in {1..60}; do
  if node -e "try { require('http').get('http://localhost:8787', () => {}).on('error', () => {}); } catch(e) {}" 2>/dev/null; then
    echo "Wrangler is ready!"
    break
  fi
  sleep 1
done

# Keep container running by waiting indefinitely
echo "Container is ready. Keeping service running..."
sleep infinity