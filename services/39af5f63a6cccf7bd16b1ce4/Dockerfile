FROM python:3.6-slim
ENV PYTHONUNBUFFERED=1
RUN mkdir /web && apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*
WORKDIR /web
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy all source files and directories
COPY . /web/
EXPOSE 8100
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8100", "-w", "6", "-t", "0"]