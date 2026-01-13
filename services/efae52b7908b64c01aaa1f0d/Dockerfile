FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential libcurl4-openssl-dev libxml2-dev libxslt1-dev libpq-dev python3-dev && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1

COPY . .

RUN pip install MarkupSafe==2.0.1 Werkzeug==0.16.1 itsdangerous==0.24 .[all]

EXPOSE 5000

CMD ["pyspider", "all"]
