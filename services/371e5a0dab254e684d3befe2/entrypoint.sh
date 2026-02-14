#!/bin/bash
set -e

echo "Starting Cascadia Code font build..."
python build.py --web-fonts

echo "Font build complete. Starting web server..."
exec python web_server.py