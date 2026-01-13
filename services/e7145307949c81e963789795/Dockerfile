FROM python:3.10-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV RASA_PORT=5000

# Copy requirements first for better caching
# Use custom requirements that exclude matplotlib (only needed for evaluation, not server)
# and upgrade PyYAML and boto3 to versions compatible with Python 3.10
# boto3 1.5.20 has old vendored urllib3 incompatible with Python 3.10's collections module changes
COPY alt_requirements/requirements_bare.txt /tmp/requirements_bare.txt
RUN sed -e '/matplotlib/d' -e 's/pyyaml==5.4/pyyaml==5.1/' -e 's/boto3==1.5.20/boto3>=1.28.0/' -e 's/klein==17.10.0/klein==23.12.0/' -e 's/hyperlink==/hyperlink>=/' /tmp/requirements_bare.txt > requirements.txt && rm /tmp/requirements_bare.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install sklearn for intent classification
RUN pip install --no-cache-dir scikit-learn

# Install spaCy for NLP processing
RUN pip install --no-cache-dir spacy

# Copy application code
COPY . .

# Expose internal port
EXPOSE 5000

# Set the command to start the Rasa NLU server
CMD ["python", "-m", "rasa_nlu.server", "--config", "config.yml", "--port", "5000", "--path", "/app/models"]