FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/home/ubuntu/deploy-projects/17c85e969e78bbd137850133/src
ENV NLTK_DATA=/home/ubuntu/deploy-projects/17c85e969e78bbd137850133/nltk_data

WORKDIR /home/ubuntu/deploy-projects/17c85e969e78bbd137850133

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy minimal web requirements
COPY requirements-web.txt .

# Install web service dependencies
RUN pip install --no-cache-dir -r requirements-web.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True)"

# Create version file for nlpia
COPY src/nlpia src/nlpia
RUN echo '__version__ = "1.0.0"' > src/nlpia/_version.py

COPY . .

# Expose the service port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the Flask app
CMD ["python", "app.py"]