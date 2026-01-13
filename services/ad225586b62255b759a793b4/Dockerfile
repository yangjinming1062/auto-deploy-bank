# Use the official Python image.
FROM python:3.11-slim

# Set the working directory.
WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy the dependencies file and install them.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose the port the app runs on.
EXPOSE 7860

# The command to run the application.
CMD ["python", "ChuanhuChatbot.py"]

