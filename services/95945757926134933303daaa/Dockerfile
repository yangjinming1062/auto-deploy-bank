# Baseimage
FROM python:3.12.10-slim-bookworm

# Environment
ENV PYTHONUNBUFFERED=1

# Update Packages and install curl and build-essential
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY ./requirements.txt /CrewAI-Studio/requirements.txt
WORKDIR /CrewAI-Studio
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY ./ /CrewAI-Studio/

# Expose Streamlit port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "./app/app.py", "--server.headless", "true"]