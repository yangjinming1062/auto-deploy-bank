FROM python:3.10-slim

# Install curl, git and Xvfb for virtual display
RUN apt-get update && apt-get install -y curl git xvfb && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Initialize git submodules with HTTPS URL conversion
RUN git config --global url."https://github.com/".insteadOf git@github.com: && \
    git clone --recursive https://github.com/747929791/majsoul_wrapper.git majsoul_wrapper || echo "majsoul_wrapper clone skipped" && \
    git clone --recursive https://github.com/747929791/MahjongAI.git JianYangAI || echo "JianYangAI clone skipped"

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the AI socket server port
EXPOSE 7479

# Run the main service with Linux compatibility fix
CMD ["/app/entrypoint.sh"]