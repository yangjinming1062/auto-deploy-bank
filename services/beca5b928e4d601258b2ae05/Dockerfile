FROM python:2.7-slim

# Install curl and mysql client for healthcheck and db import
RUN echo "deb http://archive.debian.org/debian/ buster main\ndeb http://archive.debian.org/debian-security buster/updates main" > /etc/apt/sources.list && apt-get update && apt-get install -y curl default-mysql-client netcat && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY Install/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
