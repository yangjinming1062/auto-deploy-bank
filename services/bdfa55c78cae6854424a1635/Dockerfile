FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /home/ubuntu/deploy-projects/bdfa55c78cae6854424a1635

COPY anthropic-chat/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY anthropic-chat/ .

EXPOSE 8000

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]