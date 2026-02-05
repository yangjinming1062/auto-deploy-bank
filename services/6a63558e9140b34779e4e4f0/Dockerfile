FROM python:3.11-slim

# Install curl for healthcheck and build dependencies
RUN apt-get update && apt-get install -y curl gcc g++ make && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

WORKDIR /home/ubuntu/deploy-projects/6a63558e9140b34779e4e4f0

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose default Flet web port
EXPOSE 50166

# Run the application with web mode enabled
CMD ["./start.sh"]