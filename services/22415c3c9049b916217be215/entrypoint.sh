#!/bin/bash
# Entrypoint script to run both web server and bot

# Start web server in background
echo "Starting status server on port 8080..."
python web_server.py &
WEB_PID=$!

# Start the main bot
echo "Starting train ticket bot..."
python fuckeverything.py &
BOT_PID=$!

# Wait for either process to exit
wait $WEB_PID $BOT_PID