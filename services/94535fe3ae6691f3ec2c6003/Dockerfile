FROM python:3.11-slim

# Install curl and npm
RUN apt-get update && apt-get install -y curl npm && rm -rf /var/lib/apt/lists/*

# Install Azure Functions Core Tools v4
RUN npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Set PYTHONUNBUFFERED for proper log output
ENV PYTHONUNBUFFERED=1
# Add func to PATH
ENV PATH="/usr/local/bin:${PATH}"

# Set the working directory
WORKDIR /home/site/wwwroot

# Copy requirements first for better layer caching
COPY demo-python/code/custom-vectorizer/api/functions/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY demo-python/code/custom-vectorizer/api/functions/ .

# Create models directory and download the embedding model
ENV SENTENCE_TRANSFORMERS_TEXT_EMBEDDING_MODEL=all-MiniLM-L6-v2
RUN mkdir -p models && \
    python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save('models/all-MiniLM-L6-v2')"

# Expose the Azure Functions port (default 7071)
EXPOSE 7071

# Set the command to start the Azure Functions host
CMD ["func", "start", "--port", "7071"]