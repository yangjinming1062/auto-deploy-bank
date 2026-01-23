FROM python:3.11-slim

WORKDIR /home/ubuntu/deploy-projects/064c577695a85f79b755d68e

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Copy requirements first for better caching
COPY Agent/Tutorials/DeepResearch/requirement.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy application code
COPY Agent/Tutorials/DeepResearch/ .

# Expose the Streamlit port
EXPOSE 8501

# Run Streamlit application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]